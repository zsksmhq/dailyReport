#       这个文件是用来看fstate值的
import json
import base64


def main():
    F_STATE_Former=""
    F_State_Former_str = str(base64.b64decode(F_STATE_Former), encoding='utf-8')
    F_STATE_Former_dict = json.loads(F_State_Former_str)
    print(F_STATE_Former)


if __name__ == '__main__':
    main()