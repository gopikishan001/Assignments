import 'package:flutter/material.dart';
import 'package:weight_tracker/utils/fireBaseHelper.dart';
import 'package:weight_tracker/utils/globalData.dart';

import '../screens/addWeight.dart';

class ItemCard extends StatefulWidget {
  final String itemKey;
  final Function() notifyParent;

  const ItemCard({Key? key, required this.notifyParent, required this.itemKey})
      : super(key: key);

  @override
  State<ItemCard> createState() => _ItemCardState();
}

class _ItemCardState extends State<ItemCard> {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 8, right: 8, top: 8),
      child: InkWell(
        onTap: () async {
          await Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => AddWeight(itemKey: widget.itemKey),
              ));
          widget.notifyParent();
        },
        child: Container(
            padding: const EdgeInsets.all(15),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(10),
              color: Colors.grey[200],
            ),
            height: 85,
            child: Row(
              children: [
                const Icon(
                  Icons.circle_outlined,
                ),
                const SizedBox(width: 40),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text("weight : ${docMap[widget.itemKey]![weight_key]} kg",
                        textScaleFactor: 1.2,
                        style: TextStyle(
                          fontStyle: FontStyle.normal,
                          fontSize: 18,
                          color: Colors.purple[800],
                        )),
                    const SizedBox(height: 8),
                    Text(
                        "${docMap[widget.itemKey]![date_key]}-${docMap[widget.itemKey]![month_key]}-${docMap[widget.itemKey]![year_key]}",
                        style: const TextStyle(
                          fontSize: 15,
                          fontStyle: FontStyle.normal,
                          color: Colors.black,
                        )),
                  ],
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      InkWell(
                          onTap: () async {
                            await fireBaseHelper().deleteItem(widget.itemKey);
                            widget.notifyParent();
                          },
                          child: const Icon(
                            Icons.delete_outlined,
                            size: 30,
                          ))
                    ],
                  ),
                )
              ],
            )),
      ),
    );
  }
}
