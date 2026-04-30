import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import PublicationStatus
from app.schemas.movie import MovieCreate, MovieUpdate
from app.services.movie import movie_service


class TestMovieService:
    """Tests for movie service CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_movie(self, db_session: AsyncSession):
        """Create movie with title, description, status."""
        movie_data = MovieCreate(
            title="Test Movie",
            description="A test movie description",
            publication_status=PublicationStatus.DRAFT,
        )
        movie = await movie_service.create(db_session, movie_data)

        assert movie.id is not None
        assert movie.title == "Test Movie"
        assert movie.description == "A test movie description"
        assert movie.publication_status == PublicationStatus.DRAFT

    @pytest.mark.asyncio
    async def test_create_movie_default_draft(self, db_session: AsyncSession):
        """Default status is DRAFT."""
        movie_data = MovieCreate(
            title="Default Status Movie",
            description="Testing default status",
        )
        movie = await movie_service.create(db_session, movie_data)

        assert movie.publication_status == PublicationStatus.DRAFT

    @pytest.mark.asyncio
    async def test_get_by_id_exists(self, db_session: AsyncSession):
        """Get movie returns correct movie."""
        movie_data = MovieCreate(
            title="Get Test Movie",
            description="To be retrieved",
        )
        created = await movie_service.create(db_session, movie_data)

        found = await movie_service.get_by_id(db_session, created.id)

        assert found is not None
        assert found.id == created.id
        assert found.title == "Get Test Movie"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, db_session: AsyncSession):
        """Get non-existent movie returns None."""
        found = await movie_service.get_by_id(db_session, 99999)

        assert found is None

    @pytest.mark.asyncio
    async def test_get_all(self, db_session: AsyncSession):
        """List all movies including unpublished."""
        # Create movies with different statuses
        await movie_service.create(
            db_session,
            MovieCreate(title="Draft Movie", publication_status=PublicationStatus.DRAFT),
        )
        await movie_service.create(
            db_session,
            MovieCreate(title="Published Movie", publication_status=PublicationStatus.PUBLISHED),
        )
        await movie_service.create(
            db_session,
            MovieCreate(title="Disabled Movie", publication_status=PublicationStatus.DISABLED),
        )

        movies = await movie_service.get_all(db_session)

        assert len(movies) == 3
        titles = {m.title for m in movies}
        assert "Draft Movie" in titles
        assert "Published Movie" in titles
        assert "Disabled Movie" in titles

    @pytest.mark.asyncio
    async def test_get_published(self, db_session: AsyncSession):
        """Only published movies returned."""
        # Create movies with different statuses
        await movie_service.create(
            db_session,
            MovieCreate(title="Draft Movie 2", publication_status=PublicationStatus.DRAFT),
        )
        await movie_service.create(
            db_session,
            MovieCreate(title="Published Movie 2", publication_status=PublicationStatus.PUBLISHED),
        )
        await movie_service.create(
            db_session,
            MovieCreate(title="Published Movie 3", publication_status=PublicationStatus.PUBLISHED),
        )
        await movie_service.create(
            db_session,
            MovieCreate(title="Disabled Movie 2", publication_status=PublicationStatus.DISABLED),
        )

        movies = await movie_service.get_published(db_session)

        assert len(movies) == 2
        for movie in movies:
            assert movie.publication_status == PublicationStatus.PUBLISHED

    @pytest.mark.asyncio
    async def test_update_title(self, db_session: AsyncSession):
        """Update only title."""
        created = await movie_service.create(
            db_session,
            MovieCreate(title="Original Title", description="Original desc"),
        )

        updated = await movie_service.update(
            db_session, created.id, MovieUpdate(title="Updated Title")
        )

        assert updated is not None
        assert updated.title == "Updated Title"
        assert updated.description == "Original desc"  # Unchanged

    @pytest.mark.asyncio
    async def test_update_description(self, db_session: AsyncSession):
        """Update only description."""
        created = await movie_service.create(
            db_session,
            MovieCreate(title="Title", description="Original description"),
        )

        updated = await movie_service.update(
            db_session, created.id, MovieUpdate(description="New description")
        )

        assert updated is not None
        assert updated.title == "Title"  # Unchanged
        assert updated.description == "New description"

    @pytest.mark.asyncio
    async def test_update_status(self, db_session: AsyncSession):
        """Update publication status."""
        created = await movie_service.create(
            db_session,
            MovieCreate(title="Status Test", publication_status=PublicationStatus.DRAFT),
        )

        updated = await movie_service.update(
            db_session,
            created.id,
            MovieUpdate(publication_status=PublicationStatus.PUBLISHED),
        )

        assert updated is not None
        assert updated.publication_status == PublicationStatus.PUBLISHED

    @pytest.mark.asyncio
    async def test_update_partial(self, db_session: AsyncSession):
        """Partial update only modifies provided fields."""
        created = await movie_service.create(
            db_session,
            MovieCreate(
                title="Partial Test",
                description="Original description",
                publication_status=PublicationStatus.DRAFT,
            ),
        )

        # Update only title and status, leave description unchanged
        updated = await movie_service.update(
            db_session,
            created.id,
            MovieUpdate(title="Updated Partial", publication_status=PublicationStatus.PUBLISHED),
        )

        assert updated is not None
        assert updated.title == "Updated Partial"
        assert updated.description == "Original description"  # Unchanged
        assert updated.publication_status == PublicationStatus.PUBLISHED

    @pytest.mark.asyncio
    async def test_update_not_found(self, db_session: AsyncSession):
        """Update non-existent movie returns None."""
        updated = await movie_service.update(
            db_session, 99999, MovieUpdate(title="Does not exist")
        )

        assert updated is None

    @pytest.mark.asyncio
    async def test_delete(self, db_session: AsyncSession):
        """Hard delete removes movie."""
        created = await movie_service.create(
            db_session,
            MovieCreate(title="To Delete"),
        )

        deleted = await movie_service.delete(db_session, created.id)

        assert deleted is True

        # Verify it's gone
        found = await movie_service.get_by_id(db_session, created.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_delete_not_found(self, db_session: AsyncSession):
        """Delete non-existent returns False."""
        deleted = await movie_service.delete(db_session, 99999)

        assert deleted is False


class TestPublicationStatusTransitions:
    """Tests for publication status transitions."""

    @pytest.mark.asyncio
    async def test_draft_to_published(self, db_session: AsyncSession):
        """Transition from draft to published."""
        created = await movie_service.create(
            db_session,
            MovieCreate(title="Draft to Published", publication_status=PublicationStatus.DRAFT),
        )

        updated = await movie_service.update(
            db_session,
            created.id,
            MovieUpdate(publication_status=PublicationStatus.PUBLISHED),
        )

        assert updated.publication_status == PublicationStatus.PUBLISHED

    @pytest.mark.asyncio
    async def test_published_to_disabled(self, db_session: AsyncSession):
        """Transition from published to disabled (soft delete)."""
        created = await movie_service.create(
            db_session,
            MovieCreate(title="Published to Disabled", publication_status=PublicationStatus.PUBLISHED),
        )

        updated = await movie_service.update(
            db_session,
            created.id,
            MovieUpdate(publication_status=PublicationStatus.DISABLED),
        )

        assert updated.publication_status == PublicationStatus.DISABLED

    @pytest.mark.asyncio
    async def test_disabled_movie_not_in_published_list(self, db_session: AsyncSession):
        """Disabled movies are not returned in published list."""
        created = await movie_service.create(
            db_session,
            MovieCreate(title="Disabled Movie", publication_status=PublicationStatus.DISABLED),
        )

        published_movies = await movie_service.get_published(db_session)

        titles = [m.title for m in published_movies]
        assert "Disabled Movie" not in titles

    @pytest.mark.asyncio
    async def test_disabled_movie_can_be_hard_deleted(self, db_session: AsyncSession):
        """Movies with DISABLED status can be hard deleted."""
        created = await movie_service.create(
            db_session,
            MovieCreate(title="Delete After Disable", publication_status=PublicationStatus.DISABLED),
        )

        deleted = await movie_service.delete(db_session, created.id)

        assert deleted is True
        found = await movie_service.get_by_id(db_session, created.id)
        assert found is None
