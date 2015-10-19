from nameko.rpc import RpcProxy


class BaseService:
    storage_rpc = RpcProxy('localstorage_service')

    def save(self, section_name, new_content):
        section = self.storage_rpc.get_all(section_name)
        for field, value in new_content.items():
            if field in section:
                section[field] = value
        self.storage_rpc.set_all(section_name, section)
