import pytest

import algeria_geo as geo


def test_lookup_by_code_and_name():
    assert geo.get_wilaya(16).name_fr == "Alger"
    assert geo.get_wilaya("05").name_en == "Batna"
    assert geo.get_wilaya("Warqla").code == "30"
    assert geo.get_wilaya("تيارت").code == "14"


def test_eras():
    assert geo.get_wilaya(59).is_new_wilaya
    assert geo.get_wilaya(59, era=58) is None
    assert geo.get_wilaya(49, era=48) is None
    assert len(geo.get_wilayas()) == 69
    assert len(geo.get_wilayas(58)) == 58
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


def test_search_cross_script():
    assert geo.search("Tiaret").wilayas[0].item.code == "14"
    assert geo.search("تيارت").wilayas[0].item.code == "14"
    assert geo.search("Ouargla").wilayas[0].item.code == "30"
    assert geo.search("Warqla").wilayas[0].item.code == "30"
    assert geo.search("").wilayas == ()


def test_dropdown():
    opts = geo.to_dropdown_options("fr")
    assert opts[0] == {"value": "01", "label": "Adrar"}
    assert len(opts) == 69
