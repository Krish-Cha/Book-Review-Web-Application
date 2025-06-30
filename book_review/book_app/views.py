from django.shortcuts import render, redirect
from .models import Book, Review
from django.core.cache import cache
from django.db.models import Prefetch

def home(request):
    try:
        # Try to get from Redis cache
        books = cache.get('books_list')

        if books is None:
            # If cache miss, get from DB
            books = list(Book.objects.all().order_by('id'))
            # Save to cache (5 minutes)
            cache.set('books_list', books, timeout=300)

    except Exception as e:
        # If Redis fails, fallback to DB
        print("Redis cache error:", e)
        books = list(Book.objects.all().order_by('id'))

    return render(request, 'book_app/home.html', {'books': books})


def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        Book.objects.create(title=title, author=author)

        # Clear cache after adding book
        cache.delete('books_list')

        return redirect('home')
    return render(request, 'book_app/add_book.html')


def add_review(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(book=book, rating=rating, comment=comment)

        # Clear cache if review affects display
        cache.delete('books_list')

        return redirect('home')
    return render(request, 'book_app/add_review.html', {'book': book})
