import argparse
import logging
from typing import Any, Dict, List, Optional

from annofabapi.models import OrganizationMember, Project
from more_itertools import first_true

import annofabcli
from annofabcli import AnnofabApiFacade
from annofabcli.common.cli import AbstractCommandLineInterface, ArgumentParser, build_annofabapi_resource_and_login
from annofabcli.common.enums import FormatArgument

logger = logging.getLogger(__name__)


class ListProject(AbstractCommandLineInterface):
    """
    プロジェクト一覧を表示する。
    """

    @staticmethod
    def get_account_id_from_user_id(organization_member_list: List[OrganizationMember], user_id: str) -> Optional[str]:
        member = first_true(organization_member_list, pred=lambda e: e["user_id"] == user_id)
        if member is not None:
            return member["account_id"]
        else:
            return None

    def _modify_project_query(self, organization_name: str, project_query: Dict[str, Any]) -> Dict[str, Any]:
        """
        プロジェクト索クエリを修正する。
        ``user_id`` から ``account_id`` に変換する。
        ``except_user_id`` から ``except_account_id`` に変換する。
        ``page`` , ``limit``を削除」する

        Args:

            project_query: タスク検索クエリ（IN/OUT）

        Returns:
            修正したタスク検索クエリ

        """

        def remove_key(arg_key: str):
            if arg_key in project_query:
                logger.info(f"project_query から、`{arg_key}`　キーを削除しました。")
                project_query.pop(arg_key)

        remove_key("page")
        remove_key("limit")

        organization_member_list = self.service.wrapper.get_all_organization_members(organization_name)

        if "user_id" in project_query:
            user_id = project_query["user_id"]
            account_id = self.get_account_id_from_user_id(organization_member_list, user_id)
            if account_id is not None:
                project_query["account_id"] = account_id
            else:
                logger.warning(f"project_query に含まれている user_id: {user_id} のユーザが見つかりませんでした。")

        if "except_user_id" in project_query:
            except_user_id = project_query["except_user_id"]
            except_account_id = self.get_account_id_from_user_id(organization_member_list, except_user_id)
            if except_account_id is not None:
                project_query["except_account_id"] = except_account_id
            else:
                logger.warning(f"project_query に含まれている except_user_id: {except_user_id} のユーザが見つかりませんでした。")

        return project_query

    def get_project_list_from_organization(
        self, organization_name: str, project_query: Optional[Dict[str, Any]] = None
    ) -> List[Project]:
        """
        組織名からプロジェクト一覧を取得する。
        """

        if project_query is not None:
            project_query = self._modify_project_query(organization_name, project_query)

        logger.debug(f"project_query: {project_query}")
        project_list = self.service.wrapper.get_all_projects_of_organization(
            organization_name, query_params=project_query
        )
        return project_list

    def get_project_list_from_project_id(self, project_id_list: List[str]) -> List[Project]:
        """
        project_idからプロジェクト一覧を取得する。
        """
        project_list = []
        for project_id in project_id_list:
            project = self.service.wrapper.get_project_or_none(project_id)
            if project is None:
                logger.warning(f"project_id='{project_id}'のプロジェクトにアクセスできませんでした。")
                continue
            project_list.append(project)

        return project_list

    def main(self):
        args = self.args
        project_query = annofabcli.common.cli.get_json_from_args(args.project_query)
        organization_name = args.organization
        if organization_name is not None:
            project_list = self.get_project_list_from_organization(organization_name, project_query)
        else:
            assert args.project_id is not None
            project_id_list = annofabcli.common.cli.get_list_from_args(args.project_id)
            project_list = self.get_project_list_from_project_id(project_id_list)

        logger.info(f"プロジェクト一覧の件数: {len(project_list)}")
        self.print_according_to_format(project_list)


def main(args):
    service = build_annofabapi_resource_and_login()
    facade = AnnofabApiFacade(service)
    ListProject(service, facade, args).main()


def parse_args(parser: argparse.ArgumentParser):
    argument_parser = ArgumentParser(parser)

    query_group = parser.add_mutually_exclusive_group(required=True)

    query_group.add_argument(
        "-p",
        "--project_id",
        type=str,
        nargs="+",
        help="対象プロジェクトのproject_idを指定します。`file://`を先頭に付けると、project_idの一覧が記載されたファイルを指定できます。",
    )

    query_group.add_argument("-org", "--organization", type=str, help="対象の組織名を指定してください。")

    parser.add_argument(
        "--project_query",
        type=str,
        help="プロジェクトの検索クエリをJSON形式で指定します。'--organization'を指定したときのみ有効なオプションです。"
        "指定しない場合は、組織配下のすべてのプロジェクトを取得します。"
        "`file://`を先頭に付けると、JSON形式のファイルを指定できます。"
        "クエリのフォーマットは、[getProjectsOfOrganization API]"
        "(https://annofab.com/docs/api/#operation/getProjectsOfOrganization)のクエリパラメータと同じです。"
        "さらに追加で、`user_id`, `except_user_id` キーも指定できます。"
        "ただし `page`, `limit`キーは指定できません。",
    )

    argument_parser.add_format(
        choices=[FormatArgument.CSV, FormatArgument.JSON, FormatArgument.PRETTY_JSON, FormatArgument.PROJECT_ID_LIST],
        default=FormatArgument.CSV,
    )
    argument_parser.add_output()
    argument_parser.add_csv_format()

    argument_parser.add_query()
    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction):
    subcommand_name = "list"
    subcommand_help = "プロジェクト一覧を出力します。"
    description = "プロジェクト一覧を出力します。"

    parser = annofabcli.common.cli.add_parser(subparsers, subcommand_name, subcommand_help, description)
    parse_args(parser)
