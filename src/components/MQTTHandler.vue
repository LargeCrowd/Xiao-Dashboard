<!-- Filename: MQTTHandler.vue -->
<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import mqtt from 'mqtt';
import ggimage from '../google-image.png';

const deviceId = ref('xiao_esp32_s3_device_id'); // Replace with actual device ID or pass it as a prop
const imageBase64 = ref(null); // Store the base64 image received from MQTT
// imageBase64 = ref(ggimage);

// Function to handle MQTT connection and message reception
const connectMQTT = () => {
	const mqttAddress = 'ws://192.168.137.1:9001';
  const client = mqtt.connect(mqttAddress);

  // Define topics based on deviceId
  const rxTopic = `sscma/v0/${deviceId.value}/rx`;

  client.on('connect', () => {
    client.subscribe(rxTopic, (err) => {
      if (err) {
        console.error(`Error subscribing to ${rxTopic}:`, err);
      } else {
        console.log(`Subscribed to ${rxTopic}`);
      }
    });
  });

  client.on('message', (topic, message) => {
    console.log(`Received message on topic ${topic}`);
    imageBase64.value = message.toString();
  });

  return client;
};

// MQTT connection handling lifecycle
let mqttClient;

onMounted(() => {
  mqttClient = connectMQTT();
});

onUnmounted(() => {
  if (mqttClient) {
    mqttClient.end();
  }
});
</script>

<template>
  <div>
    <h2>MQTT Image Viewer</h2>
    <div v-if="imageBase64">
      <img :src="`data:image/png;base64,${imageBase64}`" alt="MQTT Image" />
    </div>
    <div v-else>
      <p>No image received yet...</p>
    </div>
  </div>
</template>

<style scoped>
img {
  max-width: 100%;
  border: 1px solid #ccc;
}
</style>
