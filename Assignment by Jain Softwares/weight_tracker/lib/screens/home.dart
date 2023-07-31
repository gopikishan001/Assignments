import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:weight_tracker/screens/addWeight.dart';
import 'package:weight_tracker/screens/login.dart';
import 'package:weight_tracker/utils/fireBaseHelper.dart';
import 'package:weight_tracker/widgets/itemCard.dart';

import '../utils/globalData.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool loading = true;
  String name = "";
  @override
  initState() {
    super.initState();
    User? user = FirebaseAuth.instance.currentUser;
    account_id = user!.email.toString();
    name = user.displayName.toString();
    refresh();
  }

  Future<void> refresh() async {
    await fireBaseHelper().getItemList();
    loading = false;
    setState(() {});

    return Future.delayed(const Duration(milliseconds: 500));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(name),
          actions: [
            InkWell(
                onTap: () {
                  signout();
                  showTost("Logged out Successfull");
                  Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                          builder: (BuildContext context) => LoginScreen()));
                },
                child: Icon(Icons.logout)),
            SizedBox(width: 15)
          ],
        ),
        body: loading
            ? const Center(child: CircularProgressIndicator())
            : Container(
                padding: EdgeInsets.fromLTRB(5, 5, 5, 0),
                child: RefreshIndicator(
                  onRefresh: refresh,
                  child: docMap.isEmpty
                      ? const Center(
                          child: Text("Add your 1st Data",
                              textScaleFactor: 1.2,
                              style: TextStyle(
                                fontStyle: FontStyle.normal,
                                fontSize: 18,
                              )),
                        )
                      : ListView.builder(
                          itemCount: docMap.length,
                          itemBuilder: (BuildContext context, int index) {
                            String key = docMap.keys.elementAt(index);

                            return ItemCard(
                                itemKey: key, notifyParent: refresh);
                          }),
                ),
              ),
        floatingActionButton: FloatingActionButton(
            onPressed: () async {
              await Navigator.push(context,
                  MaterialPageRoute(builder: (context) {
                return AddWeight(itemKey: "4004");
              }));
              setState(() {});
            },
            child: const Icon(Icons.add)));
  }

  signout() async {
    await Authentication.signOut(context: context);
  }
}
