from django.http import Http404


class HttpListViewMixin:
    def paginate_queryset(self, queryset, page_size):

        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page = self.request.GET.get("page") or 1
        try:
            page_number = int(page)
            if paginator.num_pages < page_number:
                page_number = paginator.num_pages
        except ValueError:
            if page == "last":
                page_number = paginator.num_pages
            elif page == 'first':
                page_number = 1
            else:
                raise Http404(
                    _("Page is not 'last' or , nor can it be converted to an int.")
                )

        page = paginator.page(page_number)
        return (paginator, page, page.object_list, page.has_other_pages())

