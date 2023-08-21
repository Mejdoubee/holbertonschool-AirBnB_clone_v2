#!/usr/bin/python3
'''
Entry point of the command interpreter
'''
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from datetime import datetime


class HBNBCommand(cmd.Cmd):
    '''HBNB command interpreter class'''
    prompt = "(hbnb) "
    classes = [
        "BaseModel",
        "User",
        "Place",
        "State",
        "City",
        "Amenity",
        "Review"
        ]

    def do_quit(self, args):
        '''Quit command to exit the program'''
        return True

    def do_EOF(self, args):
        '''EOF command to exit the program'''
        return True

    def emptyline(self):
        '''An empty line + ENTER shouldn’t execute anything'''
        pass

    def help_quit(self):
        '''Quit command to exit the program'''
        print("Quit command to exit the program")
        print()

    def do_create(self, args):
        '''
        Creates a new instance of BaseModel
        saves it (to the JSON file) and prints the id
        '''
        if not args:
            print("** class name missing **")
            return
        else:
            args = args.split()
            if args[0] not in self.classes:
                print("** class doesn't exist **")
                return
            instance = eval(args[0])()
            for param in args[1:]:
                if '=' not in param:
                    continue
                key, value = param.split('=', 1)
                value = value.replace('\\"', '"')
                if value[0] == '\"' and value[-1] == '\"':
                    value = value[1:-1].replace('_', ' ')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                setattr(instance, key, value)
            instance.save()
            print(instance.id)

    def do_show(self, args):
        '''
        Prints the string representation of an instance
        based on the class name and id
        '''
        if not args:
            print("** class name missing **")
            return
        else:
            args = args.split()
            class_name = args[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            dict_obj = storage.all()
            key = f"{class_name}.{instance_id}"
            if key not in dict_obj:
                print("** no instance found **")
                return
            else:
                print(dict_obj[key])

    def do_destroy(self, args):
        '''
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        '''
        if not args:
            print("** class name missing **")
            return
        else:
            args = args.split()
            class_name = args[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            dict_obj = storage.all()
            key = f"{class_name}.{instance_id}"
            if key not in dict_obj:
                print("** no instance found **")
                return
        del dict_obj[key]
        storage.save()

    def do_all(self, args):
        '''
        Prints all string representation of all instances
        based or not on the class name
        '''

        if args:
            args = args.split()
            if args[0] not in self.classes:
                print("** class doesn't exist **")
                return
            dict_obj = storage.all()
            printed_result = [
                self.format_obj(value) for key, value in dict_obj.items()
                if key.split(".")[0] == args[0]]
            print(printed_result)
        else:
            dict_obj = storage.all()
            printed_result = [self.format_obj(value) for key, value in dict_obj.items()]
            print(printed_result)

    def format_obj(self, obj):
        '''Formats the object into the desired string representation.'''
        obj_dict = obj.to_dict()
        for key, value in obj_dict.items():
            if isinstance(value, str) and len(value) == 19 and value[10] == 'T':
                try:
                    dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
                    # Format datetime without seconds
                    obj_dict[key] = dt.strftime('%Y-%m-%d %H:%M')
                except ValueError:
                    pass
        return "[{}] ({}) {}".format(obj.__class__.__name__, obj.id, obj_dict)



    def do_update(self, args):
        '''
        Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file)
        '''
        if not args:
            print("** class name missing **")
            return
        else:
            args = args.split()
            class_name = args[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return
            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            dict_obj = storage.all()
            key = f"{class_name}.{instance_id}"
            if key not in dict_obj:
                print("** no instance found **")
                return
            if len(args) < 3:
                print("** attribute name missing **")
                return
            if len(args) < 4:
                print("** value missing **")
                return

            instance = dict_obj[key]
            setattr(instance, args[2], args[3].strip('"'))
            instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
