import 'package:flutter/material.dart';
import 'package:weight_tracker/utils/fireBaseHelper.dart';
import '../utils/globalData.dart';

class AddWeight extends StatefulWidget {
  final String itemKey;

  const AddWeight({Key? key, required this.itemKey}) : super(key: key);

  @override
  State<AddWeight> createState() => _AddWeightState();
}

class _AddWeightState extends State<AddWeight> {
  @override
  initState() {
    super.initState();
    if (widget.itemKey == "4004") {
      data = [
        DateTime.now().day.toString(),
        DateTime.now().month.toString(),
        DateTime.now().year.toString()
      ];
      weightTextController.text = "";
    } else {
      data = [
        docMap[widget.itemKey]![date_key],
        docMap[widget.itemKey]![month_key],
        docMap[widget.itemKey]![year_key]
      ];
      weightTextController.text = docMap[widget.itemKey]![weight_key];
    }
  }

  List<String> data = [];
  TextEditingController weightTextController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(widget.itemKey == "4004" ? "Add New Data" : "Edit Data"),
        ),
        body: Container(
          padding: const EdgeInsets.all(25),
          child: Column(
            children: [
              Row(
                children: [
                  Expanded(
                    flex: 3,
                    child: Text("Date : ", style: TStyle()),
                  ),
                  Expanded(
                    flex: 5,
                    child: InkWell(
                      onTap: () => selectDateFun(),
                      child: Container(
                        padding: EdgeInsets.all(15),
                        decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey)),
                        child: Text("${data[0]}-${data[1]}-${data[2]}",
                            style: TStyle()),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 15),
              SizedBox(width: 10),
              Row(
                children: [
                  Expanded(
                    flex: 3,
                    child: Text(
                      "Weight : ",
                      style: TStyle(),
                    ),
                  ),
                  Expanded(
                      flex: 5,
                      child: TextFormField(
                        style: TStyle(),
                        keyboardType: TextInputType.number,
                        controller: weightTextController,
                        decoration:
                            const InputDecoration(border: OutlineInputBorder()),
                      ))
                ],
              ),
              const SizedBox(height: 30),
              ElevatedButton(
                  style: ButtonStyle(
                      backgroundColor:
                          MaterialStateProperty.all(Colors.purple)),
                  onPressed: () {
                    save(widget.itemKey, weightTextController.text.toString(),
                        data[0], data[1], data[2]);
                    showTost("uploading data");
                  },
                  child: const Text(
                    "Save",
                    style: TextStyle(
                      fontSize: 20,
                      color: Colors.white,
                    ),
                  )),
            ],
          ),
        ));
  }

  Future<void> selectDateFun() async {
    DateTime? picked = await showDatePicker(
        firstDate: DateTime(2000),
        context: context,
        initialDate: DateTime(
          int.tryParse(data[2])!,
          int.tryParse(data[1])!,
          int.tryParse(data[0])!,
        ),
        lastDate: DateTime.now());

    if (picked != null) {
      setState(() {
        data = [
          picked.day.toString(),
          picked.month.toString(),
          picked.year.toString()
        ];
      });
    }
  }

  save(key, weight, date, month, year) async {
    await fireBaseHelper().uploadItem(key, weight, date, month, year);

    Navigator.pop(context, true);
  }

  TStyle() {
    return const TextStyle(
        fontStyle: FontStyle.normal, fontSize: 22, color: Colors.black);
  }
}
