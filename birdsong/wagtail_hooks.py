from wagtail_modeladmin.options import (ModelAdmin, ModelAdminGroup,
                                                hooks, modeladmin_register)

from birdsong.conf import BIRDSONG_ADMIN_GROUP
from birdsong.models import Campaign, Contact
from birdsong.options import CampaignAdmin


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["icons/birdsong.svg"]


class CampaignAdmin(CampaignAdmin):
    """Out of the box wagtail-compatible Admin configuration for Campaigns.

    Birdsong's CampaignAdmin core ModelAdmin
    NOTE: Designed to be imported and overridden in your app's `wagtail_hooks.py`.

    """

    model = Campaign
    menu_label = "Campaigns"
    menu_icon = "mail"
    menu_order = 200


class ContactAdmin(ModelAdmin):
    """Out of the box wagtail-compatible Admin configuration for Contacts.

    Birdsong's ContactAdmin core ModelAdmin
    NOTE: Designed to be imported and overridden in your app's `wagtail_hooks.py`.
    """

    model = Contact
    menu_label = "Contacts"
    menu_icon = "user"
    menu_order = 300
    list_display = ("email",)


def modeladmin_register_birdsong_admin_group(modeladmin_class):
    """Controls BirdsongAdminGroup's modeladmin registration behaviour"""
    return (
        modeladmin_register(modeladmin_class)
        if BIRDSONG_ADMIN_GROUP
        else modeladmin_class
    )


@modeladmin_register_birdsong_admin_group
class BirdsongAdminGroup(ModelAdminGroup):
    """
    Designed to be imported, overridden and re-registered using `modeladmin_re_register` in your
    app's `wagtail_hooks.py`.
    """

    menu_item_name = "birdsong"  # noqa:E501 needs to be explicitly defined (at this level) in order for `modeladmin_re_register` to work properly
    menu_label = "Birdsong"
    menu_icon = "birdsong"
    menu_order = 8000  # above wagtail's Reports (9000) menu item
    items = (CampaignAdmin, ContactAdmin)


def modeladmin_re_register(modeladmin_class):
    """Method for re-registering ModelAdmin or ModelAdminGroup classes with Wagtail.

    NOTE: Use it as a decorator in your app's `wagtail_hooks.py` to replace `BirdsongAdminGroup`,
    for example:
        from birdsong.wagtail_hooks import BirdsongAdminGroup, modeladmin_re_register
        @modeladmin_re_register
        class BirdsongAdminGroup(BirdsongAdminGroup):
            menu_icon = "mail"

    :param modeladmin_class: ModelAdmin class to re-register
    :type modeladmin_class: class:`wagtail_modeladmin.options.ModelAdminGroup`

    :return: Re-registered ModelAdmin class
    :rtype: class:class:`wagtail_modeladmin.options.ModelAdminGroup`
    """

    @hooks.register("construct_main_menu")
    def unregister_menu_item(request, menu_items):
        if (
            modeladmin_class.menu_item_name
        ):  # menu_item_name defined or inherited by modeladmin_class?
            earlierst_item_with_same_name = next(
                (
                    item
                    for item in menu_items
                    if item.name == modeladmin_class.menu_item_name
                ),
                None,
            )  # first match or None
            menu_items[:] = [
                item for item in menu_items if (item != earlierst_item_with_same_name)
            ]  # filter out earlierst_item_with_same_name

    return modeladmin_register(modeladmin_class)
