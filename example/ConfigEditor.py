from pylucas import ConfigEditor

if __name__ == '__main__':
    test = ConfigEditor(File=r'test/config.json', Data={"Mods": {}, "Groups": {}})

    print(test)
    print(test.ToDict)

    test.SetValue('1.2.3.4', {})
    test.SetValue('2.2.3.4', "123")
    test.SetValue('3.2.3.4', "123")
    asd = test.GetValue('1.2.3.4')

    print(asd.ToDict)
    print(test.ToDict)