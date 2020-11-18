# Copyright (c) 2020, Manfred Moitzi
# License: MIT License
import pytest
from ezdxf.lldxf.tags import Tags
from ezdxf.lldxf.tagwriter import TagCollector
from ezdxf.proxygraphic import load_proxy_graphic, export_proxy_graphic, ProxyGraphic


def test_load_proxy_graphic():
    binary_data = load_proxy_graphic(Tags.from_text(DATA))
    assert len(binary_data) == 968


def test_export_proxy_graphic():
    tagwriter = TagCollector()
    binary_data = load_proxy_graphic(Tags.from_text(DATA))
    export_proxy_graphic(binary_data, tagwriter)
    s = ''.join(tag.dxfstr() for tag in tagwriter.tags)
    assert s == DATA


class TestProxyGraphic:
    @pytest.fixture(scope='class')
    def data(self) -> bytes:
        return load_proxy_graphic(Tags.from_text(DATA))

    @pytest.fixture
    def parser(self, data: bytes) -> ProxyGraphic:
        return ProxyGraphic(data)

    def test_info(self, parser: ProxyGraphic):
        indices = list(parser.info())
        assert len(indices) == 13
        index, size, type_ = indices[0]
        assert (index, size, type_) == (8, 84, 'POLYLINE_WITH_NORMALS')

    def test_multi_leader_entities(self):
        # ATTRIBUTE_TRUE_COLOR; size: 12
        # UNKNOWN_TYPE_51; size: 12
        # ATTRIBUTE_MARKER; size: 12
        # UNICODE_TEXT2; size: 200
        # UNKNOWN_TYPE_51; size: 12
        # ATTRIBUTE_LAYER; size: 12
        # ATTRIBUTE_TRUE_COLOR; size: 12
        # ATTRIBUTE_LINETYPE; size: 12
        # ATTRIBUTE_MARKER; size: 12
        # ATTRIBUTE_FILL; size: 12
        # POLYGON; size: 84
        # ATTRIBUTE_MARKER; size: 12
        # POLYLINE; size: 60
        # ATTRIBUTE_MARKER; size: 12
        # POLYLINE; size: 60
        # ATTRIBUTE_TRUE_COLOR; size: 12
        # ATTRIBUTE_LINETYPE; size: 12
        # ATTRIBUTE_LINEWEIGHT; size: 12
        # ATTRIBUTE_MARKER; size: 12
        # ATTRIBUTE_TRUE_COLOR; size: 12
        # ATTRIBUTE_LINETYPE; size: 12
        # ATTRIBUTE_LINEWEIGHT; size: 12
        # UNKNOWN_TYPE_51; size: 12
        parser = ProxyGraphic(load_proxy_graphic(Tags.from_text(MULITILEADER)))
        indices = list(parser.info())
        assert len(indices) == 23
        entities = list(parser.virtual_entities())
        assert len(entities) == 4
        text = entities[0]
        assert text.dxftype() == 'TEXT'
        assert text.dxf.text == 'W410'
        assert text.dxf.layer == '0'  # no DXF document available
        assert text.dxf.color == 256  # by layer
        assert text.dxf.linetype == 'BYLAYER'  # no DXF document available
        assert text.dxf.true_color is None

        polyline = entities[1]  # POLYGON
        assert polyline.dxftype() == 'POLYLINE'
        assert len(polyline.vertices) == 3
        assert text.dxf.layer == '0'  # no DXF document available
        assert text.dxf.color == 256  # by layer
        assert text.dxf.linetype == 'BYLAYER'  # no DXF document available
        assert polyline.is_closed is True

        polyline = entities[2]
        assert polyline.is_closed is False
        assert polyline.dxftype() == 'POLYLINE'
        assert len(polyline.vertices) == 2
        assert text.dxf.layer == '0'  # no DXF document available
        assert text.dxf.color == 256  # by layer
        assert text.dxf.linetype == 'BYLAYER'  # no DXF document available

        polyline = entities[3]
        assert polyline.is_closed is False
        assert polyline.dxftype() == 'POLYLINE'
        assert len(polyline.vertices) == 2
        assert text.dxf.layer == '0'  # no DXF document available
        assert text.dxf.color == 256  # by layer
        assert text.dxf.linetype == 'BYLAYER'  # no DXF document available

    def test_image_entities(self):
        # UNICODE_TEXT2; size: 204
        # POLYLINE; size: 132
        parser = ProxyGraphic(load_proxy_graphic(Tags.from_text(IMAGE)))
        indices = list(parser.info())
        assert len(indices) == 2

        entities = list(parser.virtual_entities())
        assert len(indices) == 2

        text = entities[0]
        assert text.dxftype() == 'TEXT'
        assert text.dxf.text == 'AcDbRasterImage'
        assert text.dxf.layer == '0'  # no DXF document available
        assert text.dxf.color == 256  # by layer
        assert text.dxf.linetype == 'BYLAYER'  # no DXF document available

        polyline = entities[1]
        assert polyline.is_closed is False
        assert polyline.dxftype() == 'POLYLINE'
        assert len(polyline.vertices) == 5
        assert text.dxf.layer == '0'  # no DXF document available
        assert text.dxf.color == 256  # by layer
        assert text.dxf.linetype == 'BYLAYER'  # no DXF document available


DATA = """160
968
310
C80300000D000000540000002000000002000000033E695D8B227240B00D3CF1FB7B5540000000000000000082C85BAC2FDE7240FB1040429FB05740000000000000000000000000000000000000000000000000000000000000F03F5400000020000000020000004AF9442AE7FA60405A2D686189715A4000000000000000
310
00C0DC003571AE5F40043422DDA4515D40000000000000000000000000000000000000000000000000000000000000F03F64000000040000001EA72DF9806A69402CE3B4E7B59D34400000000000000000770FBC9D50855E4000000000000000000000000000000000000000000000F03FB634003D352CE93FB1DDE561C5C1
310
E33F00000000000000000418DC3967E1F83F000000000C0000001200000000000000D0000000260000001F8BC5F8B8B46A40197732241FF06140000000000000000000000000000000000000000000000000000000000000F03F0943D77B25BDEF3F417457E0C451C0BF00000000000000003100370032002C003400320000
310
00000006000000010000000000000000000440000000000000F03F0000000000000000000000000000F03F00000000000000000000000000000000000000000000000000000000000000000000000041007200690061006C00000061007200690061006C002E007400740066000000000000000C00000012000000FF7F0000
310
6400000004000000813C33FBB3606A400278BF21B8F4614000000000000000009AEFA7C64B37034000000000000000000000000000000000000000000000F03F0943D77B25BDEF3F437457E0C451C0BF0000000000000000182D4454FB210940000000000C00000010000000010000000C0000001700000000000000540000
310
0020000000020000001EA72DF9806A69402CE3B4E7B59D344000000000000000001EA72DF9806A69402CE3B4E7B59D3440000000000000000000000000000000000000000000000000000000000000F03F540000002000000002000000B296839B8D1A724001000000F06355400000000000000000B296839B8D1A72400100
310
0000F0635540000000000000000000000000000000000000000000000000000000000000F03F540000002000000002000000632D073753076140FFFFFFFF2F525A400000000000000000632D073753076140FFFFFFFF2F525A40000000000000000000000000000000000000000000000000000000000000F03F5400000020
310
000000020000000960E446A3456F405AF2DBF448AB604000000000000000000960E446A3456F405AF2DBF448AB6040000000000000000000000000000000000000000000000000000000000000F03F
"""

MULITILEADER = """160
640
310
80020000170000000C00000016000000000000C00C00000033000000000000000C00000013000000993A0000C800000026000000EC2335956D6D9440F0AEEB8E7B766840000000000000000000000000000000000000000000000000000000000000F03F000000000000F03F00000000000000000000000000000000570034
310
00310030000000000004000000010000000000000000000840626666666666F23F0000000000000000000000000000F03F0000000000000000000000000000000000000000000000000000000001000000000000000000000072006F006D0061006E0073002E0073006800780000005C00000000000C000000330000000000
310
00000C000000100000001D0000000C00000016000000000000C00C00000012000000FF7F00000C00000013000000010000000C00000014000000010000005400000007000000030000000EA778BBEFF9934072D00E24B4FE694000000000000000005E00F4D6D4EB9340264DF666FD0B6B40000000000000000028C9814D17
310
04944016652748DB316A4000000000000000000C00000013000000891300003C00000006000000020000001B387D8403FF9340C41A1BB647186A400000000000000000FB0DD6A357189440F0AEEB8E7BD6684000000000000000000C00000013000000112700003C0000000600000002000000FB0DD6A357189440F0AEEB8E
310
7BD66840000000000000000080F9275C765D9440F0AEEB8E7BD6684000000000000000000C00000016000000000000C00C00000012000000FF7F00000C00000017000000000000000C000000130000009A3A00000C00000016000000000000C00C00000012000000FF7F00000C00000017000000FFFFFFFF0C000000330000
310
0000000000
"""

IMAGE = """160
344
310
5801000002000000CC0000002600000092B5D7AAA19916C0BF88551BB606F83F000000000000000000000000000000000000000000000000000000000000F03F000000000000F03F00000000000000000000000000000000410063004400620052006100730074006500720049006D0061006700650000000F000000000000
310
000000000000000000000000000000F03F0000000000000000000000000000F03F0000000000000000000000000000000000000000000000000000000000000000000000000000000074007800740000000000000084000000060000000500000092B5D7AAA19916C0BF88551BB606F83F00000000000000008A21ADA701E6
310
01C0BF88551BB606F83F00000000000000008A21ADA701E601C06095C5228F990740000000000000000092B5D7AAA19916C06095C5228F990740000000000000000092B5D7AAA19916C0BF88551BB606F83F0000000000000000
"""

if __name__ == '__main__':
    pytest.main([__file__])
