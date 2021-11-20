package com.example.socketiodemo

import Movies
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.squareup.moshi.JsonAdapter
import com.squareup.moshi.Moshi
//import com.github.nkzawa.emitter.Emitter
import io.socket.client.Socket
import kotlinx.android.synthetic.main.activity_main.*
import java.io.InputStream
//import com.github.nkzawa.socketio.client.IO;
//import com.github.nkzawa.socketio.client.Socket;
import io.socket.client.IO
import io.socket.emitter.Emitter
import org.json.JSONObject
import java.net.URISyntaxException
import com.squareup.moshi.Types
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory

class MainActivity : AppCompatActivity() {
    var mSocket: Socket? = null
    var userName: String? = null;
    lateinit var roomName: String;
    private val myType = Types.newParameterizedType(List::class.java, Movies::class.java)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        var string: String?
        try {
            val inputStream: InputStream = assets.open("source.txt")
            val size: Int = inputStream.available()
            val buffer = ByteArray(size)
            inputStream.read(buffer)
            string = String(buffer)
            hostTxt.setText(string)
        } catch (e: Exception) {
            Log.d("error", e.message.toString())
        }


        try {
            mSocket = IO.socket(hostTxt.text.toString())

        } catch (e: URISyntaxException) {
            Log.d("URI error", e.message.toString())
        }

        try {
            mSocket?.connect()
            result.text = "connected to " + hostTxt.text.toString() + " " + mSocket?.connected()
        } catch (e: Exception) {
            result.text = " Failed to connect. " + e.message
        }

        mSocket?.on(Socket.EVENT_CONNECT, Emitter.Listener {
            result.text = "sending"
            mSocket?.emit("messages", "hi")
        });


        mSocket?.on("notification", onNewUser) // To know if the new user entered the room.
        mSocket?.on("datasent", onDataRequest)


        // ===============

        submitName.setOnClickListener {
            userName =usernameTxt.text.toString()
            mSocket?.emit("username", userName)
            result.text = "registering " + userName
        }

        sendBtn.setOnClickListener {
            val toPerson = toTxt.text
            val msg = msgTxt.text
            val jsonstring : String  = "{'to': ${toPerson}, 'message': '${msg}'}"
            result.text = jsonstring
            val jobj = JSONObject(jsonstring)
            mSocket?.emit("private_msg",jobj)

        }

        getDataBtn.setOnClickListener {
            mSocket?.emit("getTheData",userName?.toString())
        }

    }

    var onDataRequest = Emitter.Listener {
        val data = it[0] as String
        Log.d("data received", data.toString())

        // Using data class Employee2
        val moshi: Moshi = Moshi.Builder()
            .add(KotlinJsonAdapterFactory())
            .build()
        val adapter : JsonAdapter<List<Movies>> = moshi.adapter(myType)

        val dataList = adapter.fromJson(data)
        result.text = ""

        for (e in dataList ?: emptyList() ) {
            Log.i(this.toString(), "${e.title} - ${e.plot}")
            result.append("${e.title} - ${e.plot} \n")
        }
    }

    var onNewUser = Emitter.Listener {
        val message = it[0] as String
        result.text = message
    }

    override fun onDestroy() {
        super.onDestroy()
        mSocket?.disconnect()
    }
}