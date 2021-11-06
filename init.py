# 初始化脚本
from loguru import logger


class initProject:
    def __init__(self):
        self.project_name = input("输入项目名称(用于swagger中显示的项目名称):")
        self.folder_name = input("输入文件夹名称:")
        self.docker_name = input("输入docker的名称，可以简化:")
        self.git_address = input("输入GIT地址，username:password@url:")
        self.init_tool_sh()
        self.init_start_sh()

    def init_tool_sh(self):
        # init tool.sh
        project_name = self.project_name
        docker_name = self.docker_name
        folder_name = self.folder_name
        git_address = self.git_address
        port = 8000
        stop = f"docker stop {docker_name}\n"
        rm = f"docker rm -f {docker_name}\n"
        restart = f"docker restart {docker_name}\n"
        logs = f"docker logs -f --tail 50 {docker_name}\n"
        command_str = (f"cd /home/ && rm -rf {folder_name} "
                       f"&& git clone {git_address} && bash /home/{folder_name}/"
                       f"scripts/start.sh")
        run = (
            f"docker run -d -p {port}:8000 -e PROJECT_NAME={project_name} -e OPENAPI_PREFIX=/{project_name}"
            f"-v /var/log/:/home/log/ --privileged=true "
            f"--name {docker_name} "
            f'cent:uvicorn_prod sh -c "{command_str}"'
        )
        with open("./scripts/tools.sh", "w", encoding="utf-8") as f:
            f.write(stop)
            f.write(rm)
            f.write(restart)
            f.write(logs)
            f.write(run)

    def init_start_sh(self):
        # init start.sh
        folder_name = self.folder_name
        crond = f"crond\n"
        crontab = f"crontab /home/{folder_name}/scripts/rqkscron\n"
        LC_ALL = "export LC_ALL=en_US.utf-8\n"
        LANG = "export LANG=en_US.utf-8\n"
        pip = f"pip3 install -r /home/{folder_name}/requirements.txt -i https://pypi.douban.com/simple\n"
        cd = f"cd /home/{folder_name}/\n"
        start = f"uvicorn app.main:app --host 0.0.0.0"
        with open("./scripts/start.sh", "w", encoding="utf-8") as f:
            f.write(crond)
            f.write(crontab)
            f.write(LC_ALL)
            f.write(LANG)
            f.write(pip)
            f.write(cd)
            f.write(start)


if __name__ == "__main__":
    initProject()
