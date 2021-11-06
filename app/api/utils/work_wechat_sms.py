import requests
import datetime


class workWechatSms:
    host_name = "https://qyapi.weixin.qq.com/cgi-bin"

    def __init__(
        self,
        user_id="13801587423",
        corpid="wx1e49648e862a7758",
        corpsecret="H5MQZ36D1RjEfJCcS4VT8FlDezFpPk6t0lc4VkVZGwg",
        agent_id=1,
    ):
        self.user_id = user_id
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agent_id = agent_id
        self.token()

        # print(self.access_token)

    def request(self, url, data):

        response = requests.post(url, json=data)
        if response.status_code == 200:
            # print(response.json())
            return response.json()
        else:
            TimeoutError("请求超时。")

    def upload(self, data):
        url = f"{self.host_name}/media/upload?access_token={self.access_token}&type=file"

    def token(self):
        url = (f"{self.host_name}/gettoken"
               f"?corpid={self.corpid}"
               f"&corpsecret={self.corpsecret}")
        response = requests.get(url)
        # print(response.json())
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            # print(self.access_token)
        else:
            ValueError("无法得到token")

    def send(self, message, message_type="text"):
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = (
            f"{self.host_name}/message/send?access_token={self.access_token}")

        data = {
            "touser": self.user_id,
            "msgtype": "text",
            "agentid": self.agent_id,
            "safe": 0,
            "enable_id_trans": 0
        }

        if message_type == "text":
            data["text"] = {"content": f"{send_time}_{message}"}
        elif message_type == "file":
            # 先上传素材，再上传接口。
            data["file"] = {
                "media_id": "1Yv-zXfHjSjU-7LH-GwtYqDGS-zz6w22KmWAT5COgP7o"}

        print(self.request(url, data))

    def send_group(self, message):
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = (
            f"{self.host_name}/message/send?access_token={self.access_token}")
        data = {
            "touser": self.user_id,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {
                "content": f"{send_time}_{message}"
            },
            "safe": 0,
            "enable_id_trans": 0
        }
        self.request(url, data)


if __name__ == "__main__":
    r = workWechatSms()
    r.send("图片更新完成")
