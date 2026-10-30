import pytest

import algeria_geo as geo


def test_lookup_by_code_and_name():
    assert geo.get_wilaya(16).name_fr == "Alger"
    assert geo.get_wilaya("16").name_ar == "الجزائر"
    assert geo.get_wilaya("05").name_en == "Batna"
    assert geo.get_wilaya("Warqla").code == "30"
    assert geo.get_wilaya("تيارت").code == "14"
    assert geo.get_wilaya("unknown_nonexistent") is None


def test_eras():
    assert geo.get_wilaya(59).is_new_wilaya
    assert geo.get_wilaya(59, era=58) is None
    assert geo.get_wilaya(49, era=48) is None
    assert len(geo.get_wilayas()) == 69
    assert len(geo.get_wilayas(58)) == 58
    assert len(geo.get_wilayas(48)) == 48
    with pytest.raises(ValueError):
        geo.get_wilaya(1, era=50)


def test_official_commune_and_daira_coverage():
    assert len(geo.get_communes("16")) == 57
    assert geo.get_dairas("16") == []
    assert geo.get_commune("1601").daira_code is None
    assert len(geo.get_communes("59")) == 12
    assert geo.get_commune("0319").name_fr == "Aflou"
    assert geo.get_commune("0319").wilaya_code_58 == "03"
    assert sum(len(geo.get_communes(w.code)) for w in geo.get_wilayas()) == 1541


def test_daira_lookup_and_relations():
    daira = geo.get_daira("0301")
    assert daira is not None
    assert daira.code == "0301"
    assert daira.wilaya_code == "03"
    assert daira.name_ar == "الأغواط"

    communes = geo.get_communes_by_daira("0301")
    assert len(communes) > 0
    assert communes[0].daira_code == "0301"

    assert len(geo.get_all_dairas()) == 538
    assert len(geo.get_all_communes()) == 1541


def test_phone_code_and_commune_parent():
    alger = geo.get_wilaya_by_phone_code("021")
    assert alger is not None
    assert alger.code == "16"
    assert geo.get_wilaya_by_phone_code("21").code == "16"

    blida_area = geo.get_wilayas_by_phone_code("025")
    assert any(w.code == "09" for w in blida_area)
    assert any(w.code == "26" for w in blida_area)

    # Reverse parent lookup
    aflou_w69 = geo.get_wilaya_by_commune("0319", era=69)
    assert aflou_w69 is not None
    assert aflou_w69.code == "59"

    aflou_w58 = geo.get_wilaya_by_commune("0319", era=58)
    assert aflou_w58 is not None
    assert aflou_w58.code == "03"

    # Verify formerly orphan communes have assigned dairas
    assert geo.get_commune("0919").daira_code == "0926"
    assert geo.get_commune("3532").daira_code == "3502"
    assert geo.get_commune("3533").daira_code == "3502"


def test_serialization():
    w = geo.get_wilaya(16)
    d = w.to_dict()
    assert d["code"] == "16"
    assert d["name_fr"] == "Alger"
    assert d["dairas_count"] == 0

    c = geo.get_commune("1601")
    cd = c.to_dict()
    assert cd["code"] == "1601"
    assert cd["wilaya_code"] == "16"


def test_search_cross_script():
    tiaret = geo.search("Tiaret")
    assert tiaret.wilayas[0].item.code == "14"
    assert geo.search("تيارت").wilayas[0].item.code == "14"
    assert geo.search("Ouargla").wilayas[0].item.code == "30"
    assert geo.search("Warqla").wilayas[0].item.code == "30"
    assert geo.search("").wilayas == ()
    assert tiaret.best is not None
    assert tiaret.to_dict()["query"] == "Tiaret"

    # Illizi with hamza and Arabizi search
    assert geo.get_wilaya("إليزي").code == "33"
    assert geo.search("إليزي").wilayas[0].item.code == "33"
    assert geo.search("3in defla").wilayas[0].item.code == "44"
    assert geo.search("war9la").wilayas[0].item.code == "30"
    assert geo.search("5nchela").wilayas[0].item.code == "40"


def test_dropdown():
    opts = geo.to_dropdown_options("fr")
    assert opts[0] == {"value": "01", "label": "Adrar"}
    assert len(opts) == 69
    assert len(geo.to_dropdown_options("ar", era=58)) == 58


def test_postal_codes_and_coordinates():
    assert geo.get_postal_code("Alger Centre") == "16000"
    assert geo.get_postal_code("وهران") == "31000"
    c = geo.get_commune("1601")
    assert c.post_code == "16000"
    assert isinstance(c.latitude, float) and c.latitude > 35
    assert isinstance(c.longitude, float) and c.longitude > 2
