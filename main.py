import json
import os


def network_generator():
    network_name = input("Inserisci il nome della nuova rete senza spazi: ")
    os.mkdir(network_name)
    os.mkdir(network_name + "/osservazioni")
    os.mkdir(network_name + "/scenari")
    exit_condition = False
    while not exit_condition:
        number_of_central_components = int(input("Inserisci il numero di componenti centrali della rete(>0): "))
        if number_of_central_components > 0:
            links = []
            for i in range(0, number_of_central_components):
                if i == 0:
                    links.append("Li0")
                    links.append("L0i")
                if i != 0:
                    links.append("L" + str(i-1) + str(i))
                    links.append("L" + str(i) + str(i-1))
                if i == number_of_central_components - 1:
                    links.append("L" + str(i) + "f")
                    links.append("Lf" + str(i))
            print(links)
            input()
            exit_condition = True
            # Generation of "Rete_Automi" file
            count = 0
            lindx = ""
            loutdx = ""
            linsx = links[count]
            loutsx = links[count + 1]
            components = ["IC"]
            data = {"IC": {"initial": "IC-s0",
                           "states": ["IC-s0","IC-s1","IC-s2"],
                           "transitions": [
                              {
                                "name": "IC-T0",
                                "src": "IC-s0",
                                "dst": "IC-s1",
                                "in": "null",
                                "out": [["E0", linsx]]
                              },
                              {
                                "name": "IC-T1",
                                "src": "IC-s1",
                                "dst": "IC-s0",
                                "in": ["E2", loutsx],
                                "out": [["E4", linsx]]
                              },
                              {
                                "name": "IC-T2",
                                "src": "IC-s1",
                                "dst": "IC-s2",
                                "in": ["E2", loutsx],
                                "out": "null"
                              },
                              {
                                "name": "IC-T3",
                                "src": "IC-s2",
                                "dst": "IC-s0",
                                "in": "null",
                                "out": [["E4", linsx]]
                              }
                           ]}}
            for index in range(0, number_of_central_components):
                count += 2
                lindx = links[count + 1]
                loutdx = links[count]
                linsx = links[count - 2]
                loutsx = links[count - 1]
                component_name = "C" + str(index)
                components.append(component_name)
                data[component_name] = {"initial": component_name + "-s3",
                                        "states": [component_name + "-s3",component_name + "-s4",component_name + "-s5"],
                                        "transitions": [
                                              {
                                                "name": component_name + "-T4",
                                                "src": component_name + "-s3",
                                                "dst": component_name + "-s4",
                                                "in": ["E0", linsx],
                                                "out": [["E0", loutdx]]
                                              },
                                              {
                                                "name": component_name + "-T5",
                                                "src": component_name + "-s4",
                                                "dst": component_name + "-s5",
                                                "in": ["E2", lindx],
                                                "out": [["E2", loutsx]]
                                              },
                                              {
                                                "name": component_name + "-T6",
                                                "src": component_name + "-s5",
                                                "dst": component_name + "-s3",
                                                "in": ["E4", linsx],
                                                "out": [["E4", loutdx]]
                                              },
                                              {
                                                "name": component_name + "-T7",
                                                "src": component_name + "-s4",
                                                "dst": component_name + "-s3",
                                                "in": ["E2", lindx],
                                                "out": [["E2", loutsx]]
                                              }
                                            ]}
            count += 2
            lindx = ""
            loutdx = ""
            linsx = links[count - 2]
            loutsx = links[count - 1]
            data["IF"] = {"initial": "IF-s6",
                          "states": ["IF-s6","IF-s7","IF-s8"],
                          "transitions": [
                              {
                                "name": "IF-T8",
                                "src": "IF-s6",
                                "dst": "IF-s7",
                                "in": ["E0", linsx],
                                "out": [["E2", loutsx]]
                              },
                              {
                                "name": "IF-T9",
                                "src": "IF-s7",
                                "dst": "IF-s6",
                                "in": ["E4", linsx],
                                "out": "null"
                              },
                              {
                                "name": "IF-T10",
                                "src": "IF-s7",
                                "dst": "IF-s8",
                                "in": ["E4", linsx],
                                "out": "null"
                              },
                              {
                                "name": "IF-T11",
                                "src": "IF-s8",
                                "dst": "IF-s6",
                                "in": "null",
                                "out": "null"
                              }
                            ]}
            components.append("IF")
            count = 0
            for i in range(0, len(components)-1):
                lout, lin = links[count], links[count + 1]
                first_component = components[i]
                second_component = components[i + 1]
                data[lout] = {"src": first_component, "dst": second_component}
                data[lin] = {"src": second_component, "dst": first_component}
                count += 2
            with open(network_name + "/Rete_Automi.json", 'w') as outfile:
                json.dump(data, outfile)
            # Generation of "Osservabilità" file
            data1 = {"IC-T0": "o0", "IC-T1": "o2", "IC-T2": "o3", "IC-T3": "null"}
            for index in range(0, number_of_central_components):
                component_name = "C" + str(index)
                data1[component_name + "-T4"] = "null"
                data1[component_name + "-T5"] = "null"
                data1[component_name + "-T6"] = "o" + str(index) + "3"
                data1[component_name + "-T7"] = "o" + str(index) + "4"
            data1["IF-T8"] = "o1"
            data1["IF-T9"] = "o2"
            data1["IF-T10"] = "og"
            data1["IF-T11"] = "null"
            with open(network_name + "/Osservabilità.json", 'w') as outfile:
                json.dump(data1, outfile)
            # Generation of "Rilevanza" file
            data2 = {"IC-T0": "null", "IC-T1": "null", "IC-T2": "f", "IC-T3": "null"}
            for index in range(0, number_of_central_components):
                component_name = "C" + str(index)
                data2[component_name + "-T4"] = "null"
                data2[component_name + "-T5"] = "null"
                data2[component_name + "-T6"] = str(index)
                data2[component_name + "-T7"] = "null"
            data2["IF-T8"] = "null"
            data2["IF-T9"] = "null"
            data2["IF-T10"] = "g"
            data2["IF-T11"] = "null"
            with open(network_name + "/Rilevanza.json", 'w') as outfile:
                json.dump(data2, outfile)
            print("Nuova rete creata!")
        else:
            print("Numero non accettabile!")


if __name__ == '__main__':
    network_generator()
