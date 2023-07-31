import 'dart:math';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:weight_tracker/utils/globalData.dart';

class fireBaseHelper {
  final String collection_name = "weightData";
  Future getItemList() async {
    try {
      final fetchList = await FirebaseFirestore.instance
          .collection(collection_name)
          .doc(account_id)
          .get();

      docMap = Map<String, Map<String, dynamic>>.from(convert(fetchList));

      itemID = docMap.length;

      for (String key in docMap.keys) {
        int val = int.tryParse(key)!;
        itemID = max(itemID, val);
      }
    } catch (e) {
      showTost("Welcome");
    }
  }

  convert(fetchList) {
    return fetchList.data();
  }

// For uploading links

  uploadItem(key, weight, date, month, year) {
    try {
      bool newItem = false;
      if (key == "4004" || docMap.containsKey(key) == false) {
        itemID += 1;
        newItem = true;
      }

      FirebaseFirestore.instance
          .collection(collection_name)
          .doc(account_id)
          .set({
        newItem ? itemID.toString() : key: {
          weight_key: weight.toString(),
          date_key: date.toString(),
          month_key: month.toString(),
          year_key: year.toString(),
        }
      }, SetOptions(merge: true));

      docMap[newItem ? itemID.toString() : key] = {
        weight_key: weight,
        date_key: date,
        month_key: month,
        year_key: year
      };
    } catch (e) {
      print(e.toString());
      showTost("Error in uploading data");
    }
  }

  deleteItem(key) {
    FirebaseFirestore.instance
        .collection(collection_name)
        .doc(account_id)
        .update({key: FieldValue.delete()});
  }
}

showTost(data) {
  Fluttertoast.showToast(
      msg: data,
      toastLength: Toast.LENGTH_SHORT,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      textColor: Colors.white,
      backgroundColor: Color.fromARGB(255, 75, 75, 75),
      fontSize: 16.0);
}

class Authentication {
  static Future<User?> signInWithGoogle({required BuildContext context}) async {
    FirebaseAuth auth = FirebaseAuth.instance;
    User? user;

    final GoogleSignIn googleSignIn = GoogleSignIn();

    final GoogleSignInAccount? googleSignInAccount =
        await googleSignIn.signIn();

    if (googleSignInAccount != null) {
      final GoogleSignInAuthentication googleSignInAuthentication =
          await googleSignInAccount.authentication;

      final AuthCredential credential = GoogleAuthProvider.credential(
        accessToken: googleSignInAuthentication.accessToken,
        idToken: googleSignInAuthentication.idToken,
      );

      try {
        final UserCredential userCredential =
            await auth.signInWithCredential(credential);

        user = userCredential.user;
      } on FirebaseAuthException catch (e) {
        print(e);
        showTost("Auth error");
      }
    }

    return user;
  }

  static Future<void> signOut({required BuildContext context}) async {
    try {
      await FirebaseAuth.instance.signOut();
    } catch (e) {
      showTost("Logout Failed");
    }
  }
}
