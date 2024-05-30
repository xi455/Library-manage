import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from catalog.forms import RenewBookForm
from catalog.models import Author, Book, BookInstance, Genre

# Create your views here.


@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    login_url = "/accounts/login/"
    model = Book
    context_object_name = (
        "book_list"  # your own name for the list as a template variable
    )
    queryset = Book.objects.all()  # Get 5 books containing the title war
    template_name = "catalog/book_list.html"  # Specify your own template name/location
    paginate_by = 10


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = "/accounts/login/"
    model = Book
    template_name = (
        "catalog/book_detail.html"  # Specify your own template name/location
    )


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


@login_required
def borrower_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book_inst = BookInstance(
            book=book,
            borrower=request.user,
            due_back=datetime.date.today() + datetime.timedelta(weeks=3),
            status="o",
        )
        book_inst.save()
        messages.success(request, "You have successfully borrowed the book.")

        return HttpResponseRedirect(reverse("catalog:my-borrowed"))

    return render(request, "catalog/book_borrower.html", {"bookinst": book_inst})


@permission_required("catalog.can_mark_returned")
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data["renewal_date"]
            book_inst.save()
            messages.success(request, "Book renewal successful.")

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("catalog:my-borrowed"))
        
        messages.error(request, "Book renewal failed.")

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(
            initial={
                "renewal_date": proposed_renewal_date,
            }
        )

    return render(
        request,
        "catalog/book_renew_librarian.html",
        {"form": form, "bookinst": book_inst},
    )


class AuthorListView(LoginRequiredMixin, generic.ListView):
    login_url = "/accounts/login/"
    model = Author
    context_object_name = (
        "author_list"  # your own name for the list as a template variable
    )
    queryset = Author.objects.all()  # Get 5 books containing the title war
    template_name = (
        "catalog/author_list.html"  # Specify your own template name/location
    )
    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = "/accounts/login/"
    model = Author
    template_name = (
        "catalog/author_detail.html"  # Specify your own template name/location
    )


class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"
    initial = {
        "date_of_birth": "1971-11-10",
        "date_of_death": "1971-11-13",
    }
    template_name = "catalog/author_form.html"

    def get_success_url(self) -> str:
        messages.success(self.request, "Author created successfully.")
        return super().get_success_url()


class AuthorUpdate(UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("catalog:authors")
