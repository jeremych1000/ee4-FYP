# Supervisor: Stott,E. 
# Title:  Distributed Road Traffic Speed Monitoring
## Description:

Enforcing road speed limits is expensive for authorities and politically sensitive, yet speeding traffic continues to cause deaths and injuries and make pedestrians and other vulnerable road users feel unsafe. The design of traditional speed cameras means their widespread deployment on residential roads would be detrimental to the streetscape. The most common type of speed camera covers only a single location, while average speed cameras, which measure the transit time between points, are more effective but are currently only used on major routes with limited entry and exit points. 

This project will design a low-cost, distributed vehicle speed monitoring system that communities will be able to install themselves within private property next to a street. A network of peer-to-peer devices will share information about passing traffic and detect speed limit violations by the average speed method. A peer-to-peer network means that the system will not rely on a central server, which will make it more scalable and resilient. 

It is unlikely that the system would be used to issue speeding fines until it has been rigorously proven, but until then the results would be very useful for exerting public pressure to obey speed limits, particularly for identifiable commercial vehicles, and gathering statistics that communities could use to demand more formal traffic calming or enforcement methods. 

### The specific project goals would be: 
- Implement a number plate recognition system using existing computer vision algorithms on a low-cost, readily available hardware platform. 
- Set up a peer-to-peer network to share vehicle passing times and detect violations without the need for a central server. 
- Publish photo evidence of any violations 
Advanced goals could include: 
- Use the changes in the number plate geometry as the vehicle passes to detect the instantaneous speed of a vehicle. This provides a stand-alone mode that will aid adoption in areas where there isn't already an established network. 
- Implement automatic peer discovery so that each device can find its neighbours and calculate the minimum legal transit time between them using a public mapping database. 
- Add an encryption layer so that a hacker or rogue peer cannot use the network to track the movements of law-abiding vehicles. 
- Package the system so that it can be easily installed in a home by an inexperienced user. 

### Relevant skills and interest areas: 
- Computer Vision 
- Peer-to-peer networking 
- Geographical information systems 
- Encryption 
- Data privacy and ethics 
- Open-source software and hardware

  

---
---
---
---
---

### Aims & background material (student)
- To reliably detect license plates
- Communicate plates with others and store locally
- Use average speed S=D/T to calculate speed
- Check against speed limit
- If over by 10%, publish a report online (FB, Twitter, no central reporting system yet)

- Implementation likely on RPi
- Camera + IR flash (resolution?)
    - Noise reduction, edge detection, likely black and white, OCR
- Communication module
    - Custom P2P protocol or use existing
- Upload to social media or custom server 

### Student Summary of project deliverables, fallbacks & extensions (student)
- GitHub repository
- Executable to be run on RPi
- Demo showing two RPi communicating with each other to detect a speeding car
    - Upload to social media
- Software only simulation also possible (OpenCV is robust)
    - Does not need any custom communication protocol

- Standalone speed detection
    - Have some target zones and track license plate maybe?
    - May need more processing power
- Automatical decentralised p2p finding
    - Broadcast signal (similar to how wifi routers find devices)
    - When found, share license plate info and calculate speed using GMaps API
- Encrypt
    - How will communication between more devices work
- Package system
    - Compile from GitHub, or hardware package

### Summary of Risks (student)
- Turning into implementation only project when libraries for plate recognition exist
    - OpenALPR
    - OpenCV
    - Existing p2p decentralised protocol
- Solution
    - Research more into the algorithms and do my own version
    - Or do more pre/post processing

- Not testing in enough cases
    - Need sample video of low light, bright sunlight, glare, complete darkness, etc
    - Only possible with hardware
- Solution
    - Get hardware and test somewhere
    - May be difficult to do so
