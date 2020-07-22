package com.example.camgame

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button



class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val btnNormal = findViewById<Button>(R.id.normal)
        val btnEmotion = findViewById<Button>(R.id.emotion)
        val btnChoquant = findViewById<Button>(R.id.choquant)


        btnNormal.setOnClickListener{
            val intent = Intent(this, Video::class.java)
            intent.putExtra("mode", "normal")
            startActivity(intent)
        }

        btnEmotion.setOnClickListener{
            val intent = Intent(this, Video::class.java)
            intent.putExtra("mode", "emotion")
            startActivity(intent)
        }

        btnChoquant.setOnClickListener{
            val intent = Intent(this, Video::class.java)
            intent.putExtra("mode", "choquant")
            startActivity(intent)
        }


    }
}
