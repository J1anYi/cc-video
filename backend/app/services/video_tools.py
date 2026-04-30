"""Video editing tools services."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.video_tools import (
    VideoEditProject, VideoThumbnail,
    VideoAudioTrack, VideoSubtitle, VideoTemplate
)
from app.models.video_chapter import VideoChapter


class VideoToolsService:
    @staticmethod
    def create_edit_project(db, movie_id, creator_id, name):
        project = VideoEditProject(
            movie_id=movie_id,
            creator_id=creator_id,
            name=name,
            timeline={},
            output_settings={}
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_edit_projects(db, creator_id):
        return db.query(VideoEditProject).filter(
            VideoEditProject.creator_id == creator_id
        ).order_by(VideoEditProject.updated_at.desc()).all()

    @staticmethod
    def generate_thumbnails(db, movie_id, video_path, count=5):
        thumbnails = []
        for i in range(count):
            thumbnail = VideoThumbnail(
                movie_id=movie_id,
                timestamp=i * 10,
                image_url="/uploads/thumbnails/thumb_" + str(i+1) + ".jpg",
                is_auto_generated=True
            )
            db.add(thumbnail)
            thumbnails.append(thumbnail)
        db.commit()
        return thumbnails

    @staticmethod
    def get_thumbnails(db, movie_id):
        return db.query(VideoThumbnail).filter(
            VideoThumbnail.movie_id == movie_id
        ).order_by(VideoThumbnail.timestamp).all()

    @staticmethod
    def create_chapter(db, movie_id, title, start_time, end_time=None, description=None):
        max_order = db.query(VideoChapter).filter(
            VideoChapter.movie_id == movie_id
        ).count()
        chapter = VideoChapter(
            movie_id=movie_id,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            order=max_order
        )
        db.add(chapter)
        db.commit()
        db.refresh(chapter)
        return chapter

    @staticmethod
    def get_chapters(db, movie_id):
        return db.query(VideoChapter).filter(
            VideoChapter.movie_id == movie_id
        ).order_by(VideoChapter.order).all()

    @staticmethod
    def add_audio_track(db, movie_id, language_code, language_name, audio_url, is_default=False):
        track = VideoAudioTrack(
            movie_id=movie_id,
            language_code=language_code,
            language_name=language_name,
            audio_url=audio_url,
            is_default=is_default
        )
        db.add(track)
        db.commit()
        db.refresh(track)
        return track

    @staticmethod
    def get_audio_tracks(db, movie_id):
        return db.query(VideoAudioTrack).filter(
            VideoAudioTrack.movie_id == movie_id
        ).all()

    @staticmethod
    def add_subtitle(db, movie_id, language_code, language_name, subtitle_url, is_default=False):
        subtitle = VideoSubtitle(
            movie_id=movie_id,
            language_code=language_code,
            language_name=language_name,
            subtitle_url=subtitle_url,
            is_default=is_default
        )
        db.add(subtitle)
        db.commit()
        db.refresh(subtitle)
        return subtitle

    @staticmethod
    def get_subtitles(db, movie_id):
        return db.query(VideoSubtitle).filter(
            VideoSubtitle.movie_id == movie_id
        ).all()

    @staticmethod
    def create_template(db, name, category, config, creator_id=None, is_public=False):
        template = VideoTemplate(
            name=name,
            category=category,
            config=config,
            creator_id=creator_id,
            is_public=is_public
        )
        db.add(template)
        db.commit()
        db.refresh(template)
        return template

    @staticmethod
    def get_templates(db, category=None):
        query = db.query(VideoTemplate).filter(VideoTemplate.is_public == True)
        if category:
            query = query.filter(VideoTemplate.category == category)
        return query.order_by(VideoTemplate.usage_count.desc()).all()
