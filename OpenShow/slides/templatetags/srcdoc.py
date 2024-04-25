from django import template

register = template.Library()


@register.tag(name="srcdoc")
def do_srcdoc(parser, token):
    nodelist = parser.parse(("endsrcdoc",))
    parser.delete_first_token()
    return SrcdocNode(nodelist)


class SrcdocNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context)
        result = content.replace('"', '&quot;')
        return result
