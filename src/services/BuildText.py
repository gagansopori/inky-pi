

class BuildInkyText:
    def __init__(self):
        pass

    def prepare_text(self, widget_structure, widget_content):
        """
        This method parses through the content that needs to be put on the widget & then places it based on the defined
        set of rules
        :param widget_content:
        :param widget_structure:
        :return:
        """
        match widget_content.type:
            case "Weather":
                pass
            case "News":
                pass
            case "Stocks":
                pass
            case "Image":
                pass

        pass
