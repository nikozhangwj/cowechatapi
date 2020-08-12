#!/usr/bin/env python3
from argparse import ArgumentParser
from cowechatapi.cowechat_api import CoWechatAPI


def main():
    usage = "Usage: %(prog)s [options]\n" \
            "Example : %(prog)s --coid [your_coid] --secret [your_app_secret] --agentid [your_agentid] " \
            "--user [cowechat_user] --msg [content]\n" \
            "for more option in help: cowechat --help"
    parser = ArgumentParser(prog="cowechat", usage=usage)
    parser.add_argument("-i", "--companyId", dest="coid", required=True, help="Your company id.")
    parser.add_argument("-s", "--secret", dest="secret", required=True, help="Your app secret.")
    parser.add_argument("-a", "--agentId", dest="agentid", required=True, help="Your app agentid.")
    parser.add_argument("-u", "--user", dest="to_user", required=False, help="Send to user.")
    parser.add_argument("-p", "--party", dest="to_party", required=False, help="Send to party.")
    parser.add_argument("-t", "--tag", dest="to_tag", required=False, help="Send to tag.")
    parser.add_argument("-m", "--msgType", dest="msg_type", required=False,
                        help="Message type: text, image, voice, video, file.", default="text")
    parser.add_argument("-c", "--content", dest="content", required=False, help="Type text content.")
    parser.add_argument("--mediaId", dest="media_id", required=False, help="Type image,voice,video,file use media_id.")
    options = parser.parse_args()

    if not options.coid:
        raise Exception("Invalid company id.")
    if not options.secret:
        raise Exception("Invalid secret.")
    if not options.agentid:
        raise Exception("Invalid agentid.")
    if not options.to_user and not options.to_party and not options.to_tag:
        raise Exception("WARN: --user, --party, --tag cannot empty at all.")

    if options.msg_type == 'text':
        if not options.content:
            raise Exception("Invalid content")

    try:
        cowechat = CoWechatAPI(coid=options.coid, secret=options.secret, agentid=options.agentid)
        cowechat.send(msg_type=options.msg_type, content=options.content, media_id=options.media_id,
                      to_user=options.to_user, to_tag=options.to_tag, to_party=options.to_party)
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()
