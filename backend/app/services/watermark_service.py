"""Watermark service for video protection."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets
import hashlib
import json

from app.models.watermark import (
    WatermarkConfiguration, Watermark, WatermarkSession, ForensicWatermark, LeakTrace,
    WatermarkType, WatermarkPosition, WatermarkStatus
)


class WatermarkService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def configure_watermark(
        self,
        tenant_id: int,
        default_type: WatermarkType = WatermarkType.VISIBLE,
        default_position: WatermarkPosition = WatermarkPosition.BOTTOM_RIGHT,
        default_opacity: float = 0.3,
        default_scale: float = 0.15,
        custom_x: Optional[int] = None,
        custom_y: Optional[int] = None,
        forensic_enabled: bool = False,
        forensic_strength: int = 50,
        user_watermark_enabled: bool = True,
    ) -> WatermarkConfiguration:
        existing = await self.db.execute(
            select(WatermarkConfiguration).where(
                WatermarkConfiguration.tenant_id == tenant_id,
                WatermarkConfiguration.is_active == True
            )
        )
        config = existing.scalar_one_or_none()
        
        if config:
            config.default_type = default_type
            config.default_position = default_position
            config.default_opacity = default_opacity
            config.default_scale = default_scale
            config.custom_x = custom_x
            config.custom_y = custom_y
            config.forensic_enabled = forensic_enabled
            config.forensic_strength = forensic_strength
            config.user_watermark_enabled = user_watermark_enabled
            config.updated_at = datetime.utcnow()
        else:
            config = WatermarkConfiguration(
                tenant_id=tenant_id,
                default_type=default_type,
                default_position=default_position,
                default_opacity=default_opacity,
                default_scale=default_scale,
                custom_x=custom_x,
                custom_y=custom_y,
                forensic_enabled=forensic_enabled,
                forensic_strength=forensic_strength,
                user_watermark_enabled=user_watermark_enabled,
            )
            self.db.add(config)
        
        await self.db.commit()
        await self.db.refresh(config)
        return config

    async def get_configuration(self, tenant_id: int) -> Optional[WatermarkConfiguration]:
        result = await self.db.execute(
            select(WatermarkConfiguration).where(
                WatermarkConfiguration.tenant_id == tenant_id,
                WatermarkConfiguration.is_active == True
            )
        )
        return result.scalar_one_or_none()

    async def create_watermark(
        self,
        tenant_id: int,
        name: str,
        type: WatermarkType,
        image_path: Optional[str] = None,
        text_content: Optional[str] = None,
        position: WatermarkPosition = WatermarkPosition.BOTTOM_RIGHT,
        opacity: float = 0.3,
        scale: float = 0.15,
        custom_x: Optional[int] = None,
        custom_y: Optional[int] = None,
        font_size: Optional[int] = None,
        font_color: Optional[str] = None,
    ) -> Watermark:
        watermark = Watermark(
            tenant_id=tenant_id,
            name=name,
            type=type,
            image_path=image_path,
            text_content=text_content,
            position=position,
            opacity=opacity,
            scale=scale,
            custom_x=custom_x,
            custom_y=custom_y,
            font_size=font_size,
            font_color=font_color,
        )
        self.db.add(watermark)
        await self.db.commit()
        await self.db.refresh(watermark)
        return watermark

    async def list_watermarks(self, tenant_id: int) -> List[Watermark]:
        result = await self.db.execute(
            select(Watermark).where(
                Watermark.tenant_id == tenant_id,
                Watermark.status == WatermarkStatus.ACTIVE
            )
        )
        return result.scalars().all()

    async def apply_watermark(
        self,
        tenant_id: int,
        user_id: int,
        content_id: int,
        content_type: str,
        session_id: str,
        watermark_id: Optional[int] = None,
        user_specific_text: Optional[str] = None,
    ) -> WatermarkSession:
        config = await self.get_configuration(tenant_id)
        
        watermark = None
        if watermark_id:
            result = await self.db.execute(
                select(Watermark).where(Watermark.id == watermark_id)
            )
            watermark = result.scalar_one_or_none()
        
        position = watermark.position if watermark else config.default_position
        opacity = watermark.opacity if watermark else config.default_opacity
        
        watermark_data = json.dumps({
            "position": position.value,
            "opacity": opacity,
            "user_text": user_specific_text,
            "session_id": session_id,
            "user_id": user_id,
        })
        
        session = WatermarkSession(
            tenant_id=tenant_id,
            user_id=user_id,
            session_id=session_id,
            content_id=content_id,
            content_type=content_type,
            watermark_id=watermark_id,
            watermark_data=watermark_data,
            position=position,
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def generate_forensic(
        self,
        tenant_id: int,
        user_id: int,
        content_id: int,
        content_type: str,
        session_id: str,
        strength: int = 50,
        ip_address: Optional[str] = None,
        device_info: Optional[str] = None,
    ) -> ForensicWatermark:
        pattern_id = secrets.token_hex(16)
        embedded_data = hashlib.sha256(
            f"{tenant_id}:{user_id}:{content_id}:{session_id}:{pattern_id}".encode()
        ).hexdigest()
        
        forensic = ForensicWatermark(
            tenant_id=tenant_id,
            user_id=user_id,
            content_id=content_id,
            content_type=content_type,
            session_id=session_id,
            pattern_id=pattern_id,
            embedded_data=embedded_data,
            strength=strength,
            ip_address=ip_address,
            device_info=device_info,
        )
        self.db.add(forensic)
        await self.db.commit()
        await self.db.refresh(forensic)
        return forensic

    async def trace_leak(
        self,
        tenant_id: int,
        sample_data: str,
        content_id: Optional[int] = None,
    ) -> LeakTrace:
        result = await self.db.execute(
            select(ForensicWatermark).where(
                ForensicWatermark.tenant_id == tenant_id,
                ForensicWatermark.embedded_data == sample_data
            )
        )
        forensic = result.scalar_one_or_none()
        
        if forensic:
            trace = LeakTrace(
                tenant_id=tenant_id,
                content_id=forensic.content_id,
                content_type=forensic.content_type,
                forensic_watermark_id=forensic.id,
                source_user_id=forensic.user_id,
                source_session_id=forensic.session_id,
                confidence_score=1.0,
            )
            self.db.add(trace)
            await self.db.commit()
            await self.db.refresh(trace)
            return trace
        
        return None
