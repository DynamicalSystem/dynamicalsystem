from dynamicalsystem.pytests.environment import variables as environment_variables


def test_notion_is_valid(environment_variables):
    from dynamicalsystem.poohsticks.notion import Notion

    notion = Notion("tQ24.5", 100)
    assert notion.validate_content()

def test_notion_review_is_missing(environment_variables):
    from dynamicalsystem.poohsticks.notion import Notion

    notion = Notion("tQ24.5", 1)
    assert not notion.validate_content()
