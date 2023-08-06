from django.conf.urls import url, include
from django.templatetags.static import static
from django.utils.html import format_html_join

from wagtail.core import hooks

from .views import translations_list


@hooks.register("insert_editor_js")
def insert_editor_js():
    js_files = ["wagtail_localize_language_switch/js/language-switch.js"]
    return format_html_join(
        "\n",
        '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files),
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    urls = [url(r"^(\d+)/$", translations_list, name="translations_list")]

    return [
        url(
            r"^localize/language_switch/",
            include(
                (urls, "wagtail_localize_language_switch"),
                namespace="wagtail_localize_language_switch",
            ),
        )
    ]
