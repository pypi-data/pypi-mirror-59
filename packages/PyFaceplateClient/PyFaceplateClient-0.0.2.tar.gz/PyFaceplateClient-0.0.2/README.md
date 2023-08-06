# PythonEcometClient

` pip install PyFaceplateClient==0.0.1
  pip install websockets=>8.1`

from pyfaceplateclient import Client

## 1 Создать объект с необходимыми параметрами

`host="host_ip_address"
 port="port"
 login="login" 
 password="password"`

` a=ecomet.EcometClient(host, port, login, password)`

## 2 Получить все доступные имена архивов

` archives = a.get_names()`

` print(archives)`

## 3 Выбрать имена архивов с необходимыми данными, датой и количество точек.

`id_count=1                              # идентификатор запроса (на перспективу)
 archives=['archive', 'AI_0->archive']   # список имен архивов (тип данных: list)
 start_date="2020-01-13T08:46:16Z"       # дата-время начала чтения массива данных
 step_count=10                           # кол-во точек считываемых из архива
 step_size=1                             # шаг, измеряется в секундах`

`data = a.get_data(id_count, archives, start_date, step_count, step_size)`

# Example

    from pyfaceplate import Client as cli

    def main():

        #1 Create connector
    
        host="localhost"
        port="4000"
    
        a=ecomet.EcometClient(host, port, login="login", password="password")
    
        #2 Get archive names
    
        archives = a.get_names()
    
        #3 Get all data
    
        data = a.get_data(id_count=1, archives=archives, start_date="2020-01-13T08:46:16Z", step_count=100, step_size=10)
    
    retrun data