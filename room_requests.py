from xC4 import CrEaTe_ProTo, GeneRaTePk


async def build_room_open_packet(key, iv):
    fields = {
        1: 2,
        2: {
            1: 1,
            2: 15,
            3: 5,
            4: "أدم يتصل",
            5: "1",
            6: 12,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 36981056,
            15: {
                1: "IDC3",
                2: 126,
                3: "ME"
            },
            16: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000f\u000e\u0016\u0019\u001a \u001d",
            18: 2368584,
            27: 1,
            34: "\u0000\u0001",
            40: "en",
            48: 1,
            49: {
                1: 21
            },
            50: {
                1: 36981056,
                2: 2368584,
                5: 2
            }
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), "0E15", key, iv)


async def build_room_request_packet(key, iv, target_uid):
    fields = {
        1: 22,
        2: {
            1: int(target_uid)
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), "0E15", key, iv)
