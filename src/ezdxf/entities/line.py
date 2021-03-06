# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
# Created 2019-02-15
from typing import TYPE_CHECKING
from ezdxf.math import Vector, UCS, Matrix44
from ezdxf.math.transformtools import transform_thickness_and_extrusion_without_ocs
from ezdxf.lldxf.attributes import DXFAttr, DXFAttributes, DefSubclass, XType
from ezdxf.lldxf.const import DXF12, SUBCLASS_MARKER
from .dxfentity import base_class, SubclassProcessor
from .dxfgfx import DXFGraphic, acdb_entity
from .factory import register_entity

if TYPE_CHECKING:
    from ezdxf.eztypes import TagWriter, DXFNamespace

__all__ = ['Line']

acdb_line = DefSubclass('AcDbLine', {
    'start': DXFAttr(10, xtype=XType.point3d, default=(0, 0, 0)),
    'end': DXFAttr(11, xtype=XType.point3d, default=(0, 0, 0)),
    'thickness': DXFAttr(39, default=0, optional=True),
    'extrusion': DXFAttr(210, xtype=XType.point3d, default=Vector(0.0, 0.0, 1.0), optional=True),
})


@register_entity
class Line(DXFGraphic):
    """ The LINE entity represents a 3D line from `start` to `end` """
    DXFTYPE = 'LINE'
    DXFATTRIBS = DXFAttributes(base_class, acdb_entity, acdb_line)

    def load_dxf_attribs(self, processor: SubclassProcessor = None) -> 'DXFNamespace':
        """
        Adds subclass processing for 'AcDbLine', requires previous base class and 'AcDbEntity' processing by parent
        class. (internal API)
        """
        dxf = super().load_dxf_attribs(processor)
        if processor:
            tags = processor.load_dxfattribs_into_namespace(dxf, acdb_line)
            if len(tags) and not processor.r12:
                processor.log_unprocessed_tags(tags, subclass=acdb_line.name)
        return dxf

    def export_entity(self, tagwriter: 'TagWriter') -> None:
        """ Export entity specific data as DXF tags. (internal API) """
        # base class export is done by parent class
        super().export_entity(tagwriter)
        # AcDbEntity export is done by parent class
        if tagwriter.dxfversion > DXF12:
            tagwriter.write_tag2(SUBCLASS_MARKER, acdb_line.name)
        # for all DXF versions
        self.dxf.export_dxf_attribs(tagwriter, ['start', 'end', 'thickness', 'extrusion'])
        # xdata and embedded objects export will be done by parent class

    def transform(self, m: Matrix44) -> 'Line':
        """ Transform LINE entity by transformation matrix `m` inplace.

        .. versionadded:: 0.13

        """
        start, end = m.transform_vertices([self.dxf.start, self.dxf.end])
        self.dxf.start = start
        self.dxf.end = end
        transform_thickness_and_extrusion_without_ocs(self, m)
        return self

    def translate(self, dx: float, dy: float, dz: float) -> 'Line':
        """ Optimized LINE translation about `dx` in x-axis, `dy` in y-axis and `dz` in z-axis,
        returns `self` (floating interface).

        .. versionadded:: 0.13

        """
        vec = Vector(dx, dy, dz)
        self.dxf.start = vec + self.dxf.start
        self.dxf.end = vec + self.dxf.end
        return self
