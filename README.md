You can visit (https://www.amazon.fr/dp/B0FLPSRRXT) for more information.
## The books on Amazon
- Practical Introduction to IoT Architectures
- Practical Introduction to Low Power IoT Architectures

# Low-Power IoT

The Internet of Things (IoT) is undergoing rapid growth in both the number of connected devices and the volume of in-network data. This expansion makes it essential to reduce the resource and energy requirements of all network components. Energy efficiency has therefore become a key design objective to ensure the reliability, scalability, and long-term sustainability of IoT systems.

To support the deployment of an intelligent and environmentally responsible world, IoT technologies must limit their contribution to greenhouse gas emissions and carbon dioxide (CO₂) output from sensors, devices, applications, and services. For this reason, modern IoT systems must be inherently energy efficient.

In this context, we focus on the design and deployment of low and very low power IoT architectures. These “low-power aspects” span the entire IoT chain, including sensing, processing, and wireless communication. They can be achieved through:

- Power-efficient sensing – selecting low-power sensors and optimizing sensing modes and duty cycles

- Ultra-low-power processing – using energy-efficient microcontrollers, often based on RISC-V architectures

- Energy-aware communication – reducing transmitted data through compression or smart data handling to minimize transmission energy
  

# Low-Power IoT Development Platforms

To experiment with low-power IoT systems in practice, dedicated development platforms based on energy-efficient boards and system-on-chip (SoC) solutions are required. In this work, we provide two IoT development platforms based on RISC-V (ESP32C3) or Extensa LX06, LX07 architectures, namely the ESP32-C3 and ESP32 and ESP32S3

These IoT DevKits integrate the SoCs with multiple communication interfaces and support autonomous energy sources such as batteries, supercapacitors, and solar cells.

## Heltec ESP32-C3 (HT Board)

The first IoT development kit is built around the ESP32-C3, a RISC-V–based SoC that supports several wireless technologies, including Wi-Fi, Bluetooth (BT), and LoRa for long-range communication.

This DevKit also includes an interface to the Power Profiler Kit II (PPK II), which can operate in two modes:

Ammeter mode – the board is powered by its integrated battery while the PPK measures the current drawn by the system.

Source mode – the PPK supplies a calibrated voltage to power the board directly.

The ESP32-C3 SoC is integrated into an IoT board produced by Heltec. For simplicity, this board is referred to in the prepared exercises as the HT board.

Figure: IoT.CC.boards.energy.sources.png

## Heltec ESP32 WiFi LoRa V2 (ESP32 + SX1276)

The Heltec ESP32 WiFi LoRa V2 is a compact IoT development board that combines Wi-Fi, Bluetooth, and LoRa connectivity in a single platform. It integrates an ESP32 SoC, an onboard LoRa transceiver, and a small OLED display for local monitoring and debugging.

This board emphasizes power efficiency through multiple sleep modes, optimized voltage regulation, and low-power peripheral control. It is well suited for battery-powered sensing, long-range telemetry, and edge IoT applications where energy consumption must be carefully managed.

## Heltec ESP32 WiFi LoRa V4 (ESP32S3 + SX1262)

The Heltec ESP32 WiFi LoRa V4 is an enhanced low-power IoT platform that builds on the V2 while significantly improving energy efficiency and autonomy. It supports Wi-Fi, Bluetooth, and LoRa communication, making it ideal for long-range, low-data-rate IoT deployments.

A key feature of the V4 is its ultra-low deep-sleep current of approximately 15 µA, which enables long battery lifetimes in duty-cycled applications. In addition, this version integrates a solar panel interface, allowing direct connection to energy-harvesting sources and enabling fully autonomous, sustainable IoT nodes.

The complete introduction to HT board and related DevKit and the prepared exercises is provided in the main document IoT.GreenIT.2024 (pdf).
## IoT DevKits - energy provision
### HT DevKit (HelTec) 
Note that the HT board in **low_power** stage (deep-sleep) requires only about **12µA** (at 3.3V).
<p align="center">
  <img src="images/IoT.HT.DevKit.PC.source.png" width="240" title="hover text">
  <img src="images/IoT.HT.DevKit.PPK.source.png" width="240" title="accessibility text">
  <img src="images/IoT.HT.DevKit.battery.source.png" width="240" title="accessibility text">
</p>
The above HT DevKits are powered correspondigly by: USB from PC, Power Profiler source, battery source.



