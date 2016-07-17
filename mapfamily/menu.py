from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu
from models import Category, Post

class FixMenu(CMSAttachMenu):

    name = ("Fix Menu")

    def get_nodes(self, request):
        nodes = []

        for fix in Fix.objects.all():
            node = NavigationNode(
                fix.fixLongName_text,
                fix.get_absolute_url(),
                fix.pk,
            )
            import pdb; pdb.set_trace()
            nodes.append(node)
  '''          for post in Post.objects.filter(category=category):
                node2 = NavigationNode(
                    post.title,
                    post.get_absolute_url(),
                    post.pk,
                    category.pk
                )
                nodes.append(node2)
                '''
        return nodes

menu_pool.register_menu(FixMenu)
