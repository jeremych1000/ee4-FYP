### Aims & background material (student)
- To reliably detect license plates
- Communicate plates with others and store locally
- Use average speed S=D/T to calculate speed
- Check against speed limit
- If over by 10%, publish a report online (FB, Twitter, no central reporting system yet)


---
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


---
- Software only simulation also possible (OpenCV is robust)
    - Does not need any custom communication protocol


---
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


---
- Not testing in enough cases
    - Need sample video of low light, bright sunlight, glare, complete darkness, etc
    - Only possible with hardware
- Solution
    - Get hardware and test somewhere
    - May be difficult to do so
