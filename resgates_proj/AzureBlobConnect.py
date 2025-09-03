from azure.storage.blob import BlobServiceClient, ContainerClient
from typing import List
import logging


class AzureBlobClient:
    def __init__(self, connection_string: str, container_name: str, blob_service_client: BlobServiceClient, container_client: ContainerClient) -> None:

        self.connection_string = connection_string
        self.container_name = container_name

        self.blob_service_client = blob_service_client
        self.container_client = container_client


    def save_blob(self, blob_name: str, content: str) -> None:
        '''
        Salva um texto em um blob

        Args:
            - container_name: O nome do contêiner onde o blob será salvo.
            - blob_name: O nome do blob de destino. Pode incluir diretórios, por exemplo, 'diretorio/nome_do_blob'.
            - content: O conteúdo de texto a ser gravado no blob.
        '''
        try:
            self.container_client.upload_blob(name=blob_name, data=content, overwrite=True)
            logging.info(f"Save {blob_name} in container {self.container_name}.")
    
        except Exception as e:
            logging.error(f"Tentativa de salvar o blob {blob_name} no container {self.container_client} falhou: {e}")


    def read_blob(self, blob_name: str) -> bytes:
        '''
        Lê o conteúdo de um blob

        Args:
            - container_name: O nome do contêiner onde o blob será lido.
            - blob_name: O nome do blob para leitura. Pode incluir diretórios, por exemplo, 'diretorio/nome_do_blob'.

        returns:
            O conteúdo do blob em bytes.
        '''

        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            content = blob_client.download_blob().readall()

            logging.info(f"Read {blob_name} in container {self.container_name} sucessfully.")
            return content

        except Exception as e:
            logging.error(f"Tentativa de leitura do blob {blob_name} no container {self.container_client} falhou: {e}")


    def list_blob(self, folder: str = None) -> List[str]:
        '''
        Lista o nome de todos os blobs de um container

        Args:
            - container_name: O nome do contêiner onde o blobs serão listados.
            - folder: O nome de uma pasta do container para listagem. Se não especificado, lista todos os blobs do container.

        returns:
            Uma lista contendo o nome de todos os blobs listados.
        '''
        
        if folder:
            blobs = self.container_client.list_blobs(name_starts_with=folder)
        else:
            blobs = self.container_client.list_blobs()
        
        blobs_list = [blob.name for blob in blobs]
        
        return blobs_list
    
    def blob_exists(self, blob_name: str) -> bool:
        '''
        '''
 
        blobs = self.container_client.list_blobs()
        
        for blob in blobs:
            if blob.name == blob_name:
                return True
        return False
    

class AzureBlobConnect:

    @classmethod
    def connect(self, connection_string: str, container_name: str) -> AzureBlobClient:
        try:
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_client = blob_service_client.get_container_client(container=container_name)
            return AzureBlobClient(connection_string, container_name, blob_service_client, container_client)
        except Exception as e:
            logging.error(f"Erro ao estabelecer conexão com container {container_name}: {e}")


# from dotenv import load_dotenv
# import os

# load_dotenv()
# CONNECTION_STRING = os.getenv("CONNECTION_STRING")

# try:
#     blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

# except Exception as e:
#     print(f"Erro ao conectar ao container: {e}.")

# files_today = list_blob(blob_service_client, 'cessao', '2024-05-31')
# print(files_today)

# for file in files_today:
#     print(read_blob(blob_service_client, 'cessao', file))