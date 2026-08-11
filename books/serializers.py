from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор модели Автор."""

    class Meta:
        model = Author
        fields = ['id', 'last_name', 'first_name', 'middle_name', 'bio', 'birth_date']


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор модели Книга."""

    # поле для чтения (авторов у книги может быть несколько; изменять автора книги нельзя)
    authors = AuthorSerializer(many=True, read_only=True)

    # поле для записи (чтобы передать id автора на сервер)
    author_ids = serializers.ListField(
        # child = каждый элемент внутри этого списка должен быть..., IntegerField = целым числом
        child=serializers.IntegerField(),
        # id передается, но пользователь видит не id, а имя автора
        write_only=True,
        # если пользователь при создании книги не указал авторов — создается книга без авторов
        required=False
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "isbn",
            "description",
            "genre",
            "year",
            "pages",
            "authors",
            "author_ids",
            # "total_copies",
            # "available_copies",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """Создание книги."""
        # метод срабатывает, когда на сервер приходит POST-запрос (создать новую книгу)
        author_ids = validated_data.pop("author_ids", [])
        # вытаскиваем список ID авторов из полученных данных и удаляем их
        book = Book.objects.create(**validated_data)
        # создаем книгу в базе (обязательные поля: title, year, pages)
        book.authors.set(author_ids)
        # связываем созданную книгу с авторами из базы по их ID
        return book  # возвращаем созданную книгу пользователю

    def update(self, instance, validated_data):
        """Обновление книги."""
        # метод срабатывает на PUT или PATCH запрос (изменить существующую книгу)
        author_ids = validated_data.pop("author_ids", None)
        # вытаскиваем и удаляем список ID авторов, если они были переданы в запросе; иначе - оставляем None
        for attr, value in validated_data.items():
            # цикл по тем данным, которые прислал юзер в JSON-запросе на изменение книги
            setattr(instance, attr, value)  # set attribute - установить атрибут
        instance.save()  # сохранение в БД изменений в существующей книге
        if author_ids is not None:  # изменение авторов книги при редактировании книги
            instance.authors.set(author_ids)
            # присваивание нового автора отредактированной книге
        return instance  # возвращаем измененную книгу пользователю
