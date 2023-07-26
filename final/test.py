import pickle

from models.resources import TrainingServer

server_list = ["VIP3", "VIP4", "VIP5", "VIP6"]
server_objects = []
for server in server_list:
    train_server = TrainingServer(_name=server, _time=-1)
    train_server.new_train(1)
    server_objects.append(train_server)
    with open('server.pkl', 'wb') as f:
        pickle.dump(server_objects, f)
    f.close()

server_objects = TrainingServer().load_server_list()
for server in server_objects:
    if server.name == "VIP3":
        server_objects.remove(server)



