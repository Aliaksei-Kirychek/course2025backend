from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

    async def set_room_facilities(self, room_id, facilities_ids: list[int]):
        get_current_facilities = (
            select(self.model.facility_id)
            .select_from(self.model)
            .filter_by(room_id=room_id)
        )
        results = await self.session.execute(get_current_facilities)
        current_facilities_ids: list[int] = results.scalars().all()

        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_facilities_stm = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete)
                )
            )
            await self.session.execute(delete_facilities_stm)

        if ids_to_insert:
            insert_facilities_stm = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(insert_facilities_stm)
