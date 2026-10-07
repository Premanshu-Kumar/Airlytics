'use client';
import { useEffect } from 'react';
import './globals.css';

export default function Page() {
  useEffect(() => {
    

    /*
     * ========================================================
     * AIRLYTICS FRONTEND
     * ========================================================
     *
     * Currently the prediction below is a UI demonstration.
     *
     * IMPORTANT:
     * Replace the demo prediction section with your real
     * Random Forest API once the backend endpoint is ready.
     *
     * ========================================================
     */


    function getAirportCode(city) {

      const codes = {

        "Delhi": "DEL",

        "Mumbai": "BOM",

        "Banglore": "BLR",

        "Chennai": "MAA",

        "Kolkata": "CCU",

        "Cochin": "COK",

        "Hyderabad": "HYD"

      };

      return codes[city] || city.substring(0, 3).toUpperCase();

    }



    window.predictFare = async function() {

      const button =
        document.getElementById("predictBtn");

      const buttonText =
        document.getElementById("predictText");

      const buttonIcon =
        document.getElementById("predictIcon");


      const from =
        document.getElementById("fromCity").value;

      const to =
        document.getElementById("toCity").value;

      const airline =
        document.getElementById("airline").value;

      const date =
        document.getElementById("journeyDate").value;

      const stops =
        document.getElementById("stops").value;


      /*
       * ==============================================
       * BASIC VALIDATION
       * ==============================================
       */

      if (from === to) {

        alert(
          "Source and destination cannot be the same."
        );

        return;

      }


      /*
       * ==============================================
       * LOADING STATE
       * ==============================================
       */

      button.classList.add("loading");

      buttonText.innerText = "Analysing...";

      buttonIcon.innerHTML =
        '<span class="spinner"></span>';


      /*
       * Simulate model processing.
       *
       * REMOVE THIS WHEN YOUR REAL API IS CONNECTED.
       */

      await new Promise(
        resolve => setTimeout(resolve, 1400)
      );


      /*
       * ==============================================
       * DEMO PREDICTION
       * ==============================================
       *
       * This is NOT the real Random Forest model.
       *
       * It exists only so the frontend can be tested
       * before the backend API is connected.
       */

      let basePrice = 6200;


      /*
       * Airline effect
       */

      const airlineEffect = {

        "IndiGo": 500,

        "Air India": 900,

        "Jet Airways": 700,

        "SpiceJet": 350,

        "Vistara": 850,

        "Air Asia": 250,

        "GoAir": 300,

        "Kingfisher": 600

      };


      basePrice +=
        airlineEffect[airline] || 0;


      /*
       * Stops effect
       */

      basePrice +=
        Number(stops) * 700;


      /*
       * Small route variation
       */

      const routeHash =
        (
          from.length * 173 +
          to.length * 241 +
          airline.length * 97
        ) % 1800;


      basePrice += routeHash;


      /*
       * Final demo price
       */

      const price =
        Math.round(basePrice / 10) * 10;


      const minimum =
        Math.round((price * 0.90) / 10) * 10;


      const maximum =
        Math.round((price * 1.10) / 10) * 10;


      /*
       * Confidence
       */

      const confidence =
        Math.min(
          96,
          Math.max(
            82,
            90 - Number(stops) * 2
          )
        );


      /*
       * ==============================================
       * UPDATE RESULT
       * ==============================================
       */

      
      /*
       * OTA Suggestions
       */
      const otas = ["MakeMyTrip", "EaseMyTrip", "Skyscanner", "Cleartrip"];
      const otaHtml = otas.map((ota, i) => {
        const diff = (i - 1.5) * 180 + (Math.random() * 80 - 40);
        const otaPrice = Math.round((price + diff) / 10) * 10;
        const isCheapest = i === 1; // Let's make EaseMyTrip or someone cheapest for demo
        return `
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 12px; transition: 0.2s;">
            <div>
              <strong style="font-size: 16px;">${ota}</strong>
              ${isCheapest ? '<span style="margin-left: 8px; padding: 3px 8px; background: #00c853; color: white; border-radius: 20px; font-size: 10px; font-weight: bold;">BEST PRICE</span>' : ''}
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
              <strong style="font-size: 18px;">₹${otaPrice.toLocaleString("en-IN")}</strong>
              <button style="padding: 8px 16px; background: white; color: #101828; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 13px;" onmouseover="this.style.background='#f0f0f0'" onmouseout="this.style.background='white'">Book</button>
            </div>
          </div>
        `;
      }).join("");
      document.getElementById("otaList").innerHTML = otaHtml;

      document.getElementById("resultPrice")
        .innerText =
        "₹" +
        price.toLocaleString("en-IN");


      document.getElementById("resultRange")
        .innerText =
        "Expected range ₹" +
        minimum.toLocaleString("en-IN") +
        " – ₹" +
        maximum.toLocaleString("en-IN");


      document.getElementById("confidence")
        .innerText =
        confidence + "%";


      document.getElementById("resultFrom")
        .innerText =
        getAirportCode(from);


      document.getElementById("resultTo")
        .innerText =
        getAirportCode(to);


      document.getElementById("resultFromName")
        .innerText =
        from;


      document.getElementById("resultToName")
        .innerText =
        to;


      /*
       * Show result
       */

      const result =
        document.getElementById(
          "predictionResult"
        );


      result.classList.remove("visible");


      /*
       * Force animation restart
       */

      void result.offsetWidth;


      result.classList.add("visible");


      /*
       * ==============================================
       * RESET BUTTON
       * ==============================================
       */

      button.classList.remove("loading");

      buttonText.innerText =
        "Predict again";

      buttonIcon.innerHTML =
        "⚡";

    }



    /*
     * ========================================================
     * NAVBAR SCROLL EFFECT
     * ========================================================
     */

    window.addEventListener(
      "scroll",
      function () {

        const navbar =
          document.querySelector(".navbar");


        if (window.scrollY > 30) {

          navbar.style.boxShadow =
            "0 8px 30px rgba(20,30,50,0.06)";

        } else {

          navbar.style.boxShadow =
            "none";

        }

      }
    );


    /*
     * ========================================================
     * SET MINIMUM DATE
     * ========================================================
     */

    const dateInput =
      document.getElementById("journeyDate");


    if (dateInput) {

      const today =
        new Date()
          .toISOString()
          .split("T")[0];

      dateInput.min = today;

    }


    /*
     * ========================================================
     * PARALLAX FLIGHT EFFECT
     * ========================================================
     */

    document.addEventListener(
      "mousemove",
      function (event) {

        const plane =
          document.querySelector(
            ".flight-plane"
          );


        if (!plane) return;


        const x =
          (window.innerWidth / 2 - event.clientX)
          / 80;


        const y =
          (window.innerHeight / 2 - event.clientY)
          / 100;


        plane.style.marginLeft =
          `${x}px`;


        plane.style.marginTop =
          `${y}px`;

      }
    );

  
  }, []);

  return (
    <div className="airlytics-preview-page">
      

  {/* =======================================================
       NAVBAR
  ======================================================== */}

  <nav className="navbar">

    <a href="#" className="logo">

      <div className="logo-icon">

        <svg
          width="19"
          height="19"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M2 16l20-8"/>
          <path d="M22 8l-6-2-5-4-2 1 3 5-7 3-3-2-1 2 4 3 7-2 4 5 2-1-2-6z"/>
        </svg>

      </div>

      Airlytics

    </a>


    <div className="nav-links">

      <a href="#predictor">Predict</a>

      <a href="#analytics">Analytics</a>

      <a href="#ai">Explainable AI</a>

      <a href="#model">Model</a>

    </div>


    <a href="#predictor" className="nav-button">
      Try predictor →
    </a>

  </nav>



  {/* =======================================================
       HERO
  ======================================================== */}

  <section className="hero">

    <div className="hero-grid">

      <div className="hero-content">

        <div className="eyebrow">

          <span className="pulse-dot"></span>

          AI-POWERED FLIGHT INTELLIGENCE

        </div>


        <h1>

          Know the fare

          <span>before you fly.</span>

        </h1>


        <p className="hero-description">

          Airlytics uses machine learning to estimate airfare
          and explain exactly what influences your predicted
          flight price.

        </p>


        <div className="hero-buttons">

          <a href="#predictor" className="primary-btn">

            Predict my fare

            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M5 12h14"/>
              <path d="m13 6 6 6-6 6"/>
            </svg>

          </a>


          <a href="#analytics" className="secondary-btn">

            Explore analytics

          </a>

        </div>

      </div>



      {/* FLIGHT ANIMATION */}

      <div className="flight-scene">

        <div className="glow glow-1"></div>

        <div className="glow glow-2"></div>

        <div className="route-ring"></div>


        <div className="airport airport-left">

          <span className="airport-code">DEL</span>

          <span className="airport-name">
            New Delhi
          </span>

        </div>


        <div className="airport airport-right">

          <span className="airport-code">BOM</span>

          <span className="airport-name">
            Mumbai
          </span>

        </div>


        <div className="flight-plane">

          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.7"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M2 16l20-8"/>
            <path d="M22 8l-6-2-5-4-2 1 3 5-7 3-3-2-1 2 4 3 7-2 4 5 2-1-2-6z"/>
          </svg>

        </div>


        <div className="floating-card floating-price">

          <small>ESTIMATED FARE</small>

          <strong>₹7,420</strong>

        </div>


        <div className="floating-card floating-ai">

          <small>AI MODEL</small>

          <strong>90.19% R²</strong>

        </div>

      </div>

    </div>

  </section>



  {/* =======================================================
       PREDICTOR
  ======================================================== */}

  <section id="predictor" className="section predictor-section">

    <div className="container">

      <div>

        <div className="section-label">
          ✦ AI FARE ESTIMATOR
        </div>

        <h2 className="section-title">
          Predict your flight price
        </h2>

        <p className="section-description">

          Enter your journey details and let the Airlytics
          machine-learning model estimate the expected airfare.

        </p>

      </div>


      <div className="predictor-card">

        <div className="search-grid">


          {/* FROM */}

          <div className="field">

            <label>

              <span>⌖</span>

              From

            </label>

            <select id="fromCity">
              <option value="Aamby Valley City">Aamby Valley City - Aamby Valley Airport</option>
              <option value="VA74">Abu Road Airport - Abu Road Airport (VA74)</option>
              <option value="AIP">Adampur - Adampur Airport (AIP)</option>
              <option value="IXA">Agartala - Agartala - Maharaja Bir Bikram Airport (IXA)</option>
              <option value="AGX">Agatti - Agatti Airport (AGX)</option>
              <option value="AGR">Agra - Agra Airport / Agra Air Force Station (AGR)</option>
              <option value="AMD">Ahmedabad - Sardar Vallabh Patel International Airport (AMD)</option>
              <option value="AJL">Aizawl (Lengpui) - Lengpui Airport (AJL)</option>
              <option value="Aizawl">Aizawl - Tuirial Airfield</option>
              <option value="KQH">Ajmer (Kishangarh) - Kishangarh Airport Ajmer (KQH)</option>
              <option value="VI90">Akbarpur - Akbarpur Mahamaya Rajkiya Airport (VI90)</option>
              <option value="Akli">Akli - Akli Airport</option>
              <option value="AKD">Akola - Akola Airport (AKD)</option>
              <option value="HRH">Aligarh - Aligarh Airport (HRH)</option>
              <option value="IXD">Allahabad - Prayagraj Airport (IXD)</option>
              <option value="IXV">Along Airport - Along Airport (IXV)</option>
              <option value="VI18">Ambala - Ambala Air Force Station (VI18)</option>
              <option value="AHA">Ambikapur - Maa Mahamaya Airport (AHA)</option>
              <option value="VA1L">Amla - Amla Airport (VA1L)</option>
              <option value="AVR">Amravati - Amravati  Airport (AVR)</option>
              <option value="Amreli">Amreli - Amreli Airport</option>
              <option value="ATQ">Amritsar - Sri Guru Ram Das Ji International Airport (ATQ)</option>
              <option value="Angul">Angul - Savitri Jindal Airport</option>
              <option value="Arakkonam">Arakkonam - INS Rajali / Arakkonam Naval Air Station</option>
              <option value="IXU">Aurangabad - Aurangabad Airport (IXU)</option>
              <option value="Awantipura">Awantipura - Awantipura Air Force Station</option>
              <option value="AZH">Azamgarh - Azamgarh Airport (AZH)</option>
              <option value="Baghbari Gaon">Baghbari Gaon - Dinjan Airfield</option>
              <option value="Baihar">Baihar - Birwa Airstrip</option>
              <option value="Baljek Airport">Baljek Airport - Baljek Airport</option>
              <option value="RGH">Balurghat - Balurghat Airport (RGH)</option>
              <option value="VI76">Band Tal Airport - Band Tal Airport (VI76)</option>
              <option value="VE62">Bandalo - Cuttack Airport / Charbatia Air Force Station (VE62)</option>
              <option value="Bangalore">Bangalore - HAL Airport</option>
              <option value="VA51">Banswara Airport - Banswara Airport (VA51)</option>
              <option value="Barauli Khurd">Barauli Khurd - Saifai Airport</option>
              <option value="BEK">Bareilly - Bareilly Air Force Station (BEK)</option>
              <option value="VE31">Barrackpore - Barrackpore Air Force Station (VE31)</option>
              <option value="Basapur">Basapur - Baldota Koppal Aerodrome</option>
              <option value="Begusarai">Begusarai - Ulao Aerodrome</option>
              <option value="IXG">Belgaum - Belagavi Airport (IXG)</option>
              <option value="BEP">Bellary - Bellary Airport (BEP)</option>
              <option value="Bengaluru">Bengaluru - Jakkur Aerodrome</option>
              <option value="BLR">Bengaluru - Kempegowda International Airport Bengaluru (BLR)</option>
              <option value="Benti">Benti - Benti Airstrip</option>
              <option value="Berhampur (Brahmapur)">Berhampur (Brahmapur) - Berhampur Rangeilunda Airport</option>
              <option value="Bhagalpur">Bhagalpur - Bhagalpur Airport</option>
              <option value="VI88">Bhaini - Beas Airport (VI88)</option>
              <option value="BUP">Bhatinda Air Force Station - Bhatinda Air Force Station (BUP)</option>
              <option value="BHU">Bhavnagar - Bhavnagar Airport (BHU)</option>
              <option value="UKE">Bhawanipatna - Utkela Airport (UKE)</option>
              <option value="VA1E">Bhilai Airport - Bhilai Airport (VA1E)</option>
              <option value="Bhiwani">Bhiwani - Bhiwani Airport</option>
              <option value="BHO">Bhopal - Raja Bhoj International Airport (BHO)</option>
              <option value="BBI">Bhubaneswar - Biju Patnaik International Airport (BBI)</option>
              <option value="BHJ">Bhuj - Bhuj Airport (BHJ)</option>
              <option value="KUU">Bhuntar - Kullu Manali Airport (KUU)</option>
              <option value="Bhusugaon">Bhusugaon - Barbil Tonto Airstrip</option>
              <option value="IXX">Bidar - Bidar Airport / Bidar Air Force Station (IXX)</option>
              <option value="BKB">Bikaner - Nal Airport (BKB)</option>
              <option value="PAB">Bilaspur - Bilaspur Airport (PAB)</option>
              <option value="Biraich">Biraich - Andhau Airfield</option>
              <option value="VA1C">Birlagram Airport - Birlagram Airport (VA1C)</option>
              <option value="Bokaro Airport">Bokaro Airport - Bokaro Airport</option>
              <option value="VA1O">Burhar Airport - Burhar Airport (VA1O)</option>
              <option value="VE23">Burnpur Airport - Burnpur Airport (VE23)</option>
              <option value="CHINDWARA AIRFIELD">CHINDWARA AIRFIELD - CHINDWARA AIRFIELD</option>
              <option value="CCJ">Calicut - Calicut International Airport (CCJ)</option>
              <option value="Campbell Bay">Campbell Bay - Campbell Bay Airport / INS Baaz</option>
              <option value="Chabua">Chabua - Chabua Air Force Station</option>
              <option value="Chakulia Airport">Chakulia Airport - Chakulia Airport</option>
              <option value="VA1B">Chanda Airport - Chanda Airport (VA1B)</option>
              <option value="IXC">Chandigarh - Shaheed Bhagat Singh International Airport (IXC)</option>
              <option value="MAA">Chennai - Chennai International Airport (MAA)</option>
              <option value="Chennai">Chennai - Tambaram Air Force Station</option>
              <option value="VI82">Chinyalisour - Maa Ganga Airport Uttarkashi (VI82)</option>
              <option value="SDW">Chipi - Sindhudurg Airport (SDW)</option>
              <option value="CWK">Chitrakoot - Chitrakoot Airport (CWK)</option>
              <option value="Chushul">Chushul - Chushul Airstrip</option>
              <option value="CJB">Coimbatore - Coimbatore International Airport (CJB)</option>
              <option value="COH">Cooch Behar - Cooch Behar Airport (COH)</option>
              <option value="Dadiya">Dadiya - Tarpura Airfield</option>
              <option value="JLG">Dahod - Dahod Helipad (JLG)</option>
              <option value="VE54">Daltonganj Airport - Daltonganj Airport (VE54)</option>
              <option value="NMB">Daman - Daman Airport (NMB)</option>
              <option value="DEP">Daporijo - Daporijo Airport (DEP)</option>
              <option value="DBR">Darbhanga - Darbhanga Airport (DBR)</option>
              <option value="Deesa">Deesa - Deesa Airport</option>
              <option value="DED">Dehradun (Jauligrant) - Dehradun Jolly Grant Airport (DED)</option>
              <option value="DGH">Deoghar - Deoghar Airport (DGH)</option>
              <option value="Deopur">Deopur - Therubali Aerodrome</option>
              <option value="VA1J">Dhana Airport - Dhana Airport (VA1J)</option>
              <option value="DBD">Dhanbad Airport - Dhanbad Airport (DBD)</option>
              <option value="Dhenko">Dhenko - Mandla Airstrip</option>
              <option value="VA53">Dhule(Gondur) - Dhule Airport (VA53)</option>
              <option value="DIB">Dibrugarh - Dibrugarh Airport (DIB)</option>
              <option value="Diglipur">Diglipur - INS Kohassa</option>
              <option value="DMU">Dimapur - Dimapur Airport (DMU)</option>
              <option value="DIU">Diu - Diu Airport (DIU)</option>
              <option value="Doarkhol">Doarkhol - Kharagpur Airport / Kalaikunda Air Force Station</option>
              <option value="Dumka">Dumka - Sido Kanhu Airport</option>
              <option value="Durgapur">Durgapur - Durgapur Steel Plant Airport</option>
              <option value="RDP">Durgapur - Kazi Nazrul Islam Airport (RDP)</option>
              <option value="AYJ">Faizabad - Maharshi Valmiki International Airport (AYJ)</option>
              <option value="VI71">Gannan - Pinjore Airfield and Flying Club (VI71)</option>
              <option value="Gauchar">Gauchar - Gauchar Airstrip</option>
              <option value="DXN">Gautam Buddha Nagar - Noida International Airport (DXN)</option>
              <option value="GAY">Gaya - Gaya Airport (GAY)</option>
              <option value="HDO">Ghaziabad - Hindon Airport / Hindon Air Force Station (HDO)</option>
              <option value="VE41">Giridih Airport - Giridih Airport (VE41)</option>
              <option value="GDB">Gondia - Gondia Airport (GDB)</option>
              <option value="Gopinathapur">Gopinathapur - Kendujhar Airport</option>
              <option value="GOP">Gorakhpur - Gorakhpur Airport (GOP)</option>
              <option value="GUX">Guna Airport - Guna Airport (GUX)</option>
              <option value="GAU">Guwahati - Lokpriya Gopinath Bordoloi International Airport (GAU)</option>
              <option value="GWL">Gwalior - Gwalior Airport (GWL)</option>
              <option value="HWR">Halwara - Halwara International Airport (HWR)</option>
              <option value="VO52">Harihar - Harihar Airport (VO52)</option>
              <option value="HSS">Hisar - Maharaja Agrasen International Airport (HSS)</option>
              <option value="HGI">Hollongi - Itanagar Donyi Polo Hollongi Airport (HGI)</option>
              <option value="VO95">Hosur Airport - Hosur Airport (VO95)</option>
              <option value="HBX">Hubballi - Hubballi Airport (HBX)</option>
              <option value="BPM">Hyderabad - Begumpet Airport (BPM)</option>
              <option value="Hyderabad">Hyderabad - Dundigul Air Force Academy</option>
              <option value="Hyderabad">Hyderabad - Nadirgul Airport</option>
              <option value="HYD">Hyderabad - Rajiv Gandhi International Airport (HYD)</option>
              <option value="CBD">IAF Camp - Car Nicobar Air Force Base (CBD)</option>
              <option value="IMF">Imphal - Bir Tikendrajit International Airport (IMF)</option>
              <option value="IDR">Indore - Devi Ahilya Bai Holkar International Airport (IDR)</option>
              <option value="Itarbalijor">Itarbalijor - Noamundi Airport</option>
              <option value="JLR">Jabalpur - Jabalpur Airport (JLR)</option>
              <option value="JGB">Jagdalpur - Jagdalpur Airport (JGB)</option>
              <option value="JAI">Jaipur - Jaipur International Airport (JAI)</option>
              <option value="JSA">Jaisalmer Airport - Jaisalmer Airport (JSA)</option>
              <option value="JLG">Jalgaon - Jalgaon Airport (JLG)</option>
              <option value="VE44">Jalpaiguri - Hashimara Air Force Station (VE44)</option>
              <option value="IXJ">Jammu - Jammu Airport (IXJ)</option>
              <option value="JGA">Jamnagar - Jamnagar Airport (JGA)</option>
              <option value="IXW">Jamshedpur - Sonari Airport (IXW)</option>
              <option value="PYB">Jeypore - Jeypore Airport (PYB)</option>
              <option value="Jhansi Airport">Jhansi Airport - Jhansi Airport</option>
              <option value="JRG">Jharsuguda Airport - Jharsuguda Airport (JRG)</option>
              <option value="VI69">Jhunjhunu Airport - Jhunjhunu Airport (VI69)</option>
              <option value="JDH">Jodhpur - Jodhpur Airport (JDH)</option>
              <option value="JRH">Jorhat - Jorhat Airport (JRH)</option>
              <option value="SLV">Jubbarhatti - Shimla Airport (SLV)</option>
              <option value="CDP">Kadapa - Kadapa Airport (CDP)</option>
              <option value="IXH">Kailashahar - Kailashahar Airport (IXH)</option>
              <option value="SAG">Kakadi - Shirdi International Airport (SAG)</option>
              <option value="GBI">Kalaburagi - Kalaburagi Airport (GBI)</option>
              <option value="IXY">Kandla - Kandla Airport (IXY)</option>
              <option value="DHM">Kangra - Kangra Airport (DHM)</option>
              <option value="Kannur">Kannur - Kannur Heliport</option>
              <option value="CNN">Kannur - Kannur International Airport (CNN)</option>
              <option value="Kanpur">Kanpur - IIT Kanpur Airport</option>
              <option value="KNU">Kanpur - Kanpur Airport (KNU)</option>
              <option value="Kanpur">Kanpur - Kanpur Civil Airport (Old)</option>
              <option value="VA1M">Karad Airport - Karad Airport (VA1M)</option>
              <option value="VI65">Kargil - Kargil Airport (VI65)</option>
              <option value="VE67">Kargong - Mechuka Advanced Landing Ground (VE67)</option>
              <option value="Karwar, Jodhpur">Karwar, Jodhpur - Fury Airport</option>
              <option value="IXK">Keshod - Keshod Airport (IXK)</option>
              <option value="HJR">Khajuraho - Khajuraho Airport (HJR)</option>
              <option value="Khandwa">Khandwa - Khandwa Airport</option>
              <option value="Khanpura">Khanpura - Gunna Ka Pura</option>
              <option value="Khargon Govt. Airstrip">Khargon Govt. Airstrip - Khargon Govt. Airstrip</option>
              <option value="IXN">Khowai - Khowai Airport (IXN)</option>
              <option value="Kishanganj">Kishanganj - Kishanganj Airport</option>
              <option value="COK">Kochi - Cochin International Airport (COK)</option>
              <option value="Kochi">Kochi - INS Garuda / Willingdon Island Naval Air Station</option>
              <option value="KLH">Kolhapur - Kolhapur Airport (KLH)</option>
              <option value="Kolkata">Kolkata - Behala Airport</option>
              <option value="CCU">Kolkata - Netaji Subhash Chandra Bose International Airport (CCU)</option>
              <option value="KTU">Kota - Kota Airport (KTU)</option>
              <option value="VI66">Koyul - Fukche Advanced Landing Ground (VI66)</option>
              <option value="KBK">Kushinagar - Kushinagar International Airport (KBK)</option>
              <option value="Lalitpur">Lalitpur - Lalitpur Airport</option>
              <option value="LTU">Latur - Murod Kond Airport (LTU)</option>
              <option value="IXL">Leh - Leh Kushok Bakula Rimpochee Airport (IXL)</option>
              <option value="IXI">Lilabari - Lilabari North Lakhimpur Airport (IXI)</option>
              <option value="Lucknow">Lucknow - Bakshi Ka Talab Air Force Station</option>
              <option value="LKO">Lucknow - Chaudhary Charan Singh International Airport (LKO)</option>
              <option value="LUH">Ludhiana Airport - Ludhiana Airport (LUH)</option>
              <option value="Madhubani">Madhubani - Madhubani Airport</option>
              <option value="RJA">Madhurapudi - Rajahmundry Airport (RJA)</option>
              <option value="IXM">Madurai - Madurai Airport (IXM)</option>
              <option value="LDA">Malda - Malda Airport (LDA)</option>
              <option value="Mamidiyal">Mamidiyal - Viraf Airstrip</option>
              <option value="Mandvi">Mandvi - Mandvi Airport</option>
              <option value="IXE">Mangaluru - Mangaluru International Airport (IXE)</option>
              <option value="IXQ">Manik Bhandar - Kamalpur Airport (IXQ)</option>
              <option value="Marhamtabad">Marhamtabad - Marhamtabad Airport</option>
              <option value="VA2B">Meerut - Dr. Bhimrao Ambedkar Airstrip (VA2B)</option>
              <option value="Mehsana">Mehsana - Mehsana Airport</option>
              <option value="Mithapur">Mithapur - Mithapur Airport</option>
              <option value="Mohammadabad">Mohammadabad - Mohammadabad Airport</option>
              <option value="GOX">Mopa - Manohar International Airport (GOX)</option>
              <option value="MZS">Moradabad - Moradabad Airport (MZS)</option>
              <option value="VA1D">Muirpur Airport - Muirpur Airport (VA1D)</option>
              <option value="BOM">Mumbai - Chhatrapati Shivaji Maharaj International Airport (BOM)</option>
              <option value="Mumbai">Mumbai - Juhu Aerodrome</option>
              <option value="Mundra">Mundra - Mundra Airport</option>
              <option value="MZU">Muzaffarpur - Muzaffarpur Airport (MZU)</option>
              <option value="MYQ">Mysore - Mysore Airport (MYQ)</option>
              <option value="Nagarjuna Sagar">Nagarjuna Sagar - Nagarjuna Sagar Airport</option>
              <option value="VI73">Nagaur Airport - Nagaur Airport (VI73)</option>
              <option value="NAG">Nagpur - Dr. Babasaheb Ambedkar International Airport (NAG)</option>
              <option value="Naliya">Naliya - Naliya Air Force Station</option>
              <option value="VO26">Nallatinputhur - Kovilpatti Airport (VO26)</option>
              <option value="NDC">Nanded - Nanded Airport (NDC)</option>
              <option value="VI20">Narnaul Airport - Narnaul Airport (VI20)</option>
              <option value="Nashik">Nashik - Gandhinagar Airfield</option>
              <option value="ISK">Nashik - Nashik International Airport (ISK)</option>
              <option value="NMI">Navi Mumbai - Navi Mumbai International Airport (NMI)</option>
              <option value="Nawapara">Nawapara - Nawapara Airport</option>
              <option value="DEL">New Delhi - Indira Gandhi International Airport (DEL)</option>
              <option value="New Delhi">New Delhi - Safdarjung Airport</option>
              <option value="NVY">Neyveli - Neyveli Airport (NVY)</option>
              <option value="VI40">Niawal - Karnal Airport (VI40)</option>
              <option value="VA1N">Nimach Airport - Nimach Airport (VA1N)</option>
              <option value="VE36">Nuagaon Airport - Nuagaon Airport (VE36)</option>
              <option value="Nubra">Nubra - Daulat Beg Oldi Advanced Landing Ground</option>
              <option value="VI57">Nubra - Thoise Airport (VI57)</option>
              <option value="Nyoma">Nyoma - Nyoma Airstrip</option>
              <option value="VA1H">Ondwa Airport - Ondwa Airport (VA1H)</option>
              <option value="KJB">Orvakal - Kurnool Airport (KJB)</option>
              <option value="Osmanabad">Osmanabad - Osmanabad Airport</option>
              <option value="PYG">Pakyong - Pakyong Airport (PYG)</option>
              <option value="Panagarh Air Force Station">Panagarh Air Force Station - Panagarh Air Force Station</option>
              <option value="PGH">Pantnagar - Pantnagar Airport (PGH)</option>
              <option value="IXT">Pasighat - Pasighat Airport (IXT)</option>
              <option value="IXP">Pathankot - Pathankot Airport (IXP)</option>
              <option value="Patiala Airport">Patiala Airport - Patiala Airport</option>
              <option value="Patna">Patna - Bihta Air Force Station</option>
              <option value="PAT">Patna - Jay Prakash Narayan Airport (PAT)</option>
              <option value="Phalodi Air Force Station">Phalodi Air Force Station - Phalodi Air Force Station</option>
              <option value="VA2A">Phalodi Airport - Phalodi Airport (VA2A)</option>
              <option value="VI70">Pilani New Airport - Pilani New Airport (VI70)</option>
              <option value="Pithoragarh">Pithoragarh - Pithoragarh Airport</option>
              <option value="Poonch">Poonch - Poonch Airport</option>
              <option value="PBD">Porbandar - Porbandar Airport (PBD)</option>
              <option value="IXZ">Port Blair - Veer Savarkar International Airport / INS Utkrosh (IXZ)</option>
              <option value="PNY">Puducherry (Pondicherry) - Pondicherry Airport (PNY)</option>
              <option value="BMT">Pune - Baramati Airport (BMT)</option>
              <option value="Pune">Pune - Hadapsar Gliding Centre</option>
              <option value="PNQ">Pune - Pune International Airport (PNQ)</option>
              <option value="Purnea Airport">Purnea Airport - Purnea Airport</option>
              <option value="PUT">Puttaparthi - Sri Sathya Sai Airport (PUT)</option>
              <option value="Rahani">Rahani - Birasal Airport</option>
              <option value="Raichur Airport">Raichur Airport - Raichur Airport</option>
              <option value="Raigarh Airport (JSPL)">Raigarh Airport (JSPL) - Raigarh Airport (JSPL)</option>
              <option value="RPR">Raipur - Swami Vivekananda Airport (RPR)</option>
              <option value="RAJ">Rajkot - Rajkot Airport (RAJ)</option>
              <option value="HSR">Rajkot - Rajkot International Airport (HSR)</option>
              <option value="RJI">Rajouri - Rajouri Airport (RJI)</option>
              <option value="RMD">Ramagundam - Basanth Nagar Airport (RMD)</option>
              <option value="Ramnad">Ramnad - Ramnad Naval Air Station</option>
              <option value="Rampurhat">Rampurhat - Surichua Air Base</option>
              <option value="IXR">Ranchi - Birsa Munda Airport (IXR)</option>
              <option value="VA2D">Ratlam Airport - Ratlam Airport (VA2D)</option>
              <option value="RTC">Ratnagiri Airport - Ratnagiri Airport (RTC)</option>
              <option value="Raxaul Airport">Raxaul Airport - Raxaul Airport</option>
              <option value="REW">Rewa - Rewa Airport, Chorhata, REWA (REW)</option>
              <option value="RRK">Rourkela - Rourkela Airport (RRK)</option>
              <option value="Rumgara">Rumgara - Korba Airport</option>
              <option value="RUP">Rupsi - Rupsi Airport (RUP)</option>
              <option value="Saharsa">Saharsa - Saharsa Airport</option>
              <option value="SXV">Salem - Salem Airport (SXV)</option>
              <option value="Sambalpur">Sambalpur - Hirakud Airport</option>
              <option value="TNI">Satna Airport - Satna Airport (TNI)</option>
              <option value="Secunderabad">Secunderabad - Hakimpet Airport</option>
              <option value="SWN">Sherpur Naqeebpur - Sarsawa Air Force Station (SWN)</option>
              <option value="SHL">Shillong - Shillong Airport (SHL)</option>
              <option value="RQY">Shimoga - Rashtrakavi Kuvempu Airport (RQY)</option>
              <option value="Shirpur">Shirpur - Shirpur Airport</option>
              <option value="VSV">Shravasti - Shravasti Airport (VSV)</option>
              <option value="VA1F">Sidhi Airport - Sidhi Airport (VA1F)</option>
              <option value="IXS">Silchar - Silchar Airport (IXS)</option>
              <option value="IXB">Siliguri - Bagdogra Airport (IXB)</option>
              <option value="VA38">Sirohi Airport - Sirohi Airport (VA38)</option>
              <option value="Sirsa Air Force Station">Sirsa Air Force Station - Sirsa Air Force Station</option>
              <option value="VE24">Sokriting T.E. - Sookerating (Doomdooma) Airport (VE24)</option>
              <option value="SSE">Solapur - Solapur Airport (SSE)</option>
              <option value="SXR">Srinagar - Srinagar International Airport (SXR)</option>
              <option value="Sultanpur">Sultanpur - Sultanpur Airport</option>
              <option value="Sulur">Sulur - Coimbatore Air Force Station</option>
              <option value="STV">Surat - Surat International Airport (STV)</option>
              <option value="VI43">Suratgarh New Airport - Suratgarh New Airport (VI43)</option>
              <option value="Tarauna">Tarauna - Fursatganj Airport</option>
              <option value="TEZ">Tezpur Airport - Tezpur Airport (TEZ)</option>
              <option value="TEI">Tezu - Tezu Airport (TEI)</option>
              <option value="TJV">Thanjavur - Thanjavur Air Force Station (TJV)</option>
              <option value="TRV">Thiruvananthapuram - Thiruvananthapuram International Airport (TRV)</option>
              <option value="VE96">Thuniabhand Airport - Thuniabhand Airport (VE96)</option>
              <option value="TRZ">Tiruchirappalli - Tiruchirappalli International Airport (TRZ)</option>
              <option value="TIR">Tirupati - Tirupati International Airport (TIR)</option>
              <option value="VDY">Toranagallu - Jindal Vijaynagar Airport (VDY)</option>
              <option value="Tuting">Tuting - Tuting Advanced Landing Ground</option>
              <option value="UDR">Udaipur - Maharana Pratap Airport (UDR)</option>
              <option value="Udhampur">Udhampur - Udhampur Air Force Station</option>
              <option value="Ujjain">Ujjain - Bentayan Airport</option>
              <option value="Umaria">Umaria - Umaria Air Field</option>
              <option value="Uttarlai Airport">Uttarlai Airport - Uttarlai Airport</option>
              <option value="BDQ">Vadodara - Vadodara International Airport (BDQ)</option>
              <option value="TCR">Vagaikulam - Tuticorin Airport (TCR)</option>
              <option value="Vanasthali">Vanasthali - Vanasthali Airport</option>
              <option value="VNS">Varanasi - Lal Bahadur Shastri International Airport (VNS)</option>
              <option value="GOI">Vasco da Gama - Goa Dabolim International Airport (GOI)</option>
              <option value="Vedanta Lanjigarh Airstrip">Vedanta Lanjigarh Airstrip - Vedanta Lanjigarh Airstrip</option>
              <option value="Vellore">Vellore - Vellore Airport</option>
              <option value="Vijay Nagar">Vijay Nagar - Vijay Nagar Airport</option>
              <option value="VGA">Vijayawada - Vijayawada International Airport (VGA)</option>
              <option value="VE91">Vijaynagar Advanced Landing Ground - Vijaynagar Advanced Landing Ground (VE91)</option>
              <option value="VTZ">Visakhapatnam - Alluri Sitarama Raju International Airport (Vizag) (VTZ)</option>
              <option value="Visakhapatnam">Visakhapatnam - INS Dega Airport (visakhapatnam international airport)</option>
              <option value="Walong Advanced Landing Ground">Walong Advanced Landing Ground - Walong Advanced Landing Ground</option>
              <option value="WGC">Warangal - Warangal Airport (WGC)</option>
              <option value="VA78">Yavatmal - Sant Gadge Baba Yavatmal Airport (VA78)</option>
              <option value="Yelahanka">Yelahanka - Yelahanka Air Force Station</option>
              <option value="ZER">Ziro - Ziro Airport (ZER)</option>
            </select>

          </div>



          {/* TO */}

          <div className="field">

            <label>

              <span>⌖</span>

              To

            </label>

            <select id="toCity">
              <option value="Aamby Valley City">Aamby Valley City - Aamby Valley Airport</option>
              <option value="VA74">Abu Road Airport - Abu Road Airport (VA74)</option>
              <option value="AIP">Adampur - Adampur Airport (AIP)</option>
              <option value="IXA">Agartala - Agartala - Maharaja Bir Bikram Airport (IXA)</option>
              <option value="AGX">Agatti - Agatti Airport (AGX)</option>
              <option value="AGR">Agra - Agra Airport / Agra Air Force Station (AGR)</option>
              <option value="AMD">Ahmedabad - Sardar Vallabh Patel International Airport (AMD)</option>
              <option value="AJL">Aizawl (Lengpui) - Lengpui Airport (AJL)</option>
              <option value="Aizawl">Aizawl - Tuirial Airfield</option>
              <option value="KQH">Ajmer (Kishangarh) - Kishangarh Airport Ajmer (KQH)</option>
              <option value="VI90">Akbarpur - Akbarpur Mahamaya Rajkiya Airport (VI90)</option>
              <option value="Akli">Akli - Akli Airport</option>
              <option value="AKD">Akola - Akola Airport (AKD)</option>
              <option value="HRH">Aligarh - Aligarh Airport (HRH)</option>
              <option value="IXD">Allahabad - Prayagraj Airport (IXD)</option>
              <option value="IXV">Along Airport - Along Airport (IXV)</option>
              <option value="VI18">Ambala - Ambala Air Force Station (VI18)</option>
              <option value="AHA">Ambikapur - Maa Mahamaya Airport (AHA)</option>
              <option value="VA1L">Amla - Amla Airport (VA1L)</option>
              <option value="AVR">Amravati - Amravati  Airport (AVR)</option>
              <option value="Amreli">Amreli - Amreli Airport</option>
              <option value="ATQ">Amritsar - Sri Guru Ram Das Ji International Airport (ATQ)</option>
              <option value="Angul">Angul - Savitri Jindal Airport</option>
              <option value="Arakkonam">Arakkonam - INS Rajali / Arakkonam Naval Air Station</option>
              <option value="IXU">Aurangabad - Aurangabad Airport (IXU)</option>
              <option value="Awantipura">Awantipura - Awantipura Air Force Station</option>
              <option value="AZH">Azamgarh - Azamgarh Airport (AZH)</option>
              <option value="Baghbari Gaon">Baghbari Gaon - Dinjan Airfield</option>
              <option value="Baihar">Baihar - Birwa Airstrip</option>
              <option value="Baljek Airport">Baljek Airport - Baljek Airport</option>
              <option value="RGH">Balurghat - Balurghat Airport (RGH)</option>
              <option value="VI76">Band Tal Airport - Band Tal Airport (VI76)</option>
              <option value="VE62">Bandalo - Cuttack Airport / Charbatia Air Force Station (VE62)</option>
              <option value="Bangalore">Bangalore - HAL Airport</option>
              <option value="VA51">Banswara Airport - Banswara Airport (VA51)</option>
              <option value="Barauli Khurd">Barauli Khurd - Saifai Airport</option>
              <option value="BEK">Bareilly - Bareilly Air Force Station (BEK)</option>
              <option value="VE31">Barrackpore - Barrackpore Air Force Station (VE31)</option>
              <option value="Basapur">Basapur - Baldota Koppal Aerodrome</option>
              <option value="Begusarai">Begusarai - Ulao Aerodrome</option>
              <option value="IXG">Belgaum - Belagavi Airport (IXG)</option>
              <option value="BEP">Bellary - Bellary Airport (BEP)</option>
              <option value="Bengaluru">Bengaluru - Jakkur Aerodrome</option>
              <option value="BLR">Bengaluru - Kempegowda International Airport Bengaluru (BLR)</option>
              <option value="Benti">Benti - Benti Airstrip</option>
              <option value="Berhampur (Brahmapur)">Berhampur (Brahmapur) - Berhampur Rangeilunda Airport</option>
              <option value="Bhagalpur">Bhagalpur - Bhagalpur Airport</option>
              <option value="VI88">Bhaini - Beas Airport (VI88)</option>
              <option value="BUP">Bhatinda Air Force Station - Bhatinda Air Force Station (BUP)</option>
              <option value="BHU">Bhavnagar - Bhavnagar Airport (BHU)</option>
              <option value="UKE">Bhawanipatna - Utkela Airport (UKE)</option>
              <option value="VA1E">Bhilai Airport - Bhilai Airport (VA1E)</option>
              <option value="Bhiwani">Bhiwani - Bhiwani Airport</option>
              <option value="BHO">Bhopal - Raja Bhoj International Airport (BHO)</option>
              <option value="BBI">Bhubaneswar - Biju Patnaik International Airport (BBI)</option>
              <option value="BHJ">Bhuj - Bhuj Airport (BHJ)</option>
              <option value="KUU">Bhuntar - Kullu Manali Airport (KUU)</option>
              <option value="Bhusugaon">Bhusugaon - Barbil Tonto Airstrip</option>
              <option value="IXX">Bidar - Bidar Airport / Bidar Air Force Station (IXX)</option>
              <option value="BKB">Bikaner - Nal Airport (BKB)</option>
              <option value="PAB">Bilaspur - Bilaspur Airport (PAB)</option>
              <option value="Biraich">Biraich - Andhau Airfield</option>
              <option value="VA1C">Birlagram Airport - Birlagram Airport (VA1C)</option>
              <option value="Bokaro Airport">Bokaro Airport - Bokaro Airport</option>
              <option value="VA1O">Burhar Airport - Burhar Airport (VA1O)</option>
              <option value="VE23">Burnpur Airport - Burnpur Airport (VE23)</option>
              <option value="CHINDWARA AIRFIELD">CHINDWARA AIRFIELD - CHINDWARA AIRFIELD</option>
              <option value="CCJ">Calicut - Calicut International Airport (CCJ)</option>
              <option value="Campbell Bay">Campbell Bay - Campbell Bay Airport / INS Baaz</option>
              <option value="Chabua">Chabua - Chabua Air Force Station</option>
              <option value="Chakulia Airport">Chakulia Airport - Chakulia Airport</option>
              <option value="VA1B">Chanda Airport - Chanda Airport (VA1B)</option>
              <option value="IXC">Chandigarh - Shaheed Bhagat Singh International Airport (IXC)</option>
              <option value="MAA">Chennai - Chennai International Airport (MAA)</option>
              <option value="Chennai">Chennai - Tambaram Air Force Station</option>
              <option value="VI82">Chinyalisour - Maa Ganga Airport Uttarkashi (VI82)</option>
              <option value="SDW">Chipi - Sindhudurg Airport (SDW)</option>
              <option value="CWK">Chitrakoot - Chitrakoot Airport (CWK)</option>
              <option value="Chushul">Chushul - Chushul Airstrip</option>
              <option value="CJB">Coimbatore - Coimbatore International Airport (CJB)</option>
              <option value="COH">Cooch Behar - Cooch Behar Airport (COH)</option>
              <option value="Dadiya">Dadiya - Tarpura Airfield</option>
              <option value="JLG">Dahod - Dahod Helipad (JLG)</option>
              <option value="VE54">Daltonganj Airport - Daltonganj Airport (VE54)</option>
              <option value="NMB">Daman - Daman Airport (NMB)</option>
              <option value="DEP">Daporijo - Daporijo Airport (DEP)</option>
              <option value="DBR">Darbhanga - Darbhanga Airport (DBR)</option>
              <option value="Deesa">Deesa - Deesa Airport</option>
              <option value="DED">Dehradun (Jauligrant) - Dehradun Jolly Grant Airport (DED)</option>
              <option value="DGH">Deoghar - Deoghar Airport (DGH)</option>
              <option value="Deopur">Deopur - Therubali Aerodrome</option>
              <option value="VA1J">Dhana Airport - Dhana Airport (VA1J)</option>
              <option value="DBD">Dhanbad Airport - Dhanbad Airport (DBD)</option>
              <option value="Dhenko">Dhenko - Mandla Airstrip</option>
              <option value="VA53">Dhule(Gondur) - Dhule Airport (VA53)</option>
              <option value="DIB">Dibrugarh - Dibrugarh Airport (DIB)</option>
              <option value="Diglipur">Diglipur - INS Kohassa</option>
              <option value="DMU">Dimapur - Dimapur Airport (DMU)</option>
              <option value="DIU">Diu - Diu Airport (DIU)</option>
              <option value="Doarkhol">Doarkhol - Kharagpur Airport / Kalaikunda Air Force Station</option>
              <option value="Dumka">Dumka - Sido Kanhu Airport</option>
              <option value="Durgapur">Durgapur - Durgapur Steel Plant Airport</option>
              <option value="RDP">Durgapur - Kazi Nazrul Islam Airport (RDP)</option>
              <option value="AYJ">Faizabad - Maharshi Valmiki International Airport (AYJ)</option>
              <option value="VI71">Gannan - Pinjore Airfield and Flying Club (VI71)</option>
              <option value="Gauchar">Gauchar - Gauchar Airstrip</option>
              <option value="DXN">Gautam Buddha Nagar - Noida International Airport (DXN)</option>
              <option value="GAY">Gaya - Gaya Airport (GAY)</option>
              <option value="HDO">Ghaziabad - Hindon Airport / Hindon Air Force Station (HDO)</option>
              <option value="VE41">Giridih Airport - Giridih Airport (VE41)</option>
              <option value="GDB">Gondia - Gondia Airport (GDB)</option>
              <option value="Gopinathapur">Gopinathapur - Kendujhar Airport</option>
              <option value="GOP">Gorakhpur - Gorakhpur Airport (GOP)</option>
              <option value="GUX">Guna Airport - Guna Airport (GUX)</option>
              <option value="GAU">Guwahati - Lokpriya Gopinath Bordoloi International Airport (GAU)</option>
              <option value="GWL">Gwalior - Gwalior Airport (GWL)</option>
              <option value="HWR">Halwara - Halwara International Airport (HWR)</option>
              <option value="VO52">Harihar - Harihar Airport (VO52)</option>
              <option value="HSS">Hisar - Maharaja Agrasen International Airport (HSS)</option>
              <option value="HGI">Hollongi - Itanagar Donyi Polo Hollongi Airport (HGI)</option>
              <option value="VO95">Hosur Airport - Hosur Airport (VO95)</option>
              <option value="HBX">Hubballi - Hubballi Airport (HBX)</option>
              <option value="BPM">Hyderabad - Begumpet Airport (BPM)</option>
              <option value="Hyderabad">Hyderabad - Dundigul Air Force Academy</option>
              <option value="Hyderabad">Hyderabad - Nadirgul Airport</option>
              <option value="HYD">Hyderabad - Rajiv Gandhi International Airport (HYD)</option>
              <option value="CBD">IAF Camp - Car Nicobar Air Force Base (CBD)</option>
              <option value="IMF">Imphal - Bir Tikendrajit International Airport (IMF)</option>
              <option value="IDR">Indore - Devi Ahilya Bai Holkar International Airport (IDR)</option>
              <option value="Itarbalijor">Itarbalijor - Noamundi Airport</option>
              <option value="JLR">Jabalpur - Jabalpur Airport (JLR)</option>
              <option value="JGB">Jagdalpur - Jagdalpur Airport (JGB)</option>
              <option value="JAI">Jaipur - Jaipur International Airport (JAI)</option>
              <option value="JSA">Jaisalmer Airport - Jaisalmer Airport (JSA)</option>
              <option value="JLG">Jalgaon - Jalgaon Airport (JLG)</option>
              <option value="VE44">Jalpaiguri - Hashimara Air Force Station (VE44)</option>
              <option value="IXJ">Jammu - Jammu Airport (IXJ)</option>
              <option value="JGA">Jamnagar - Jamnagar Airport (JGA)</option>
              <option value="IXW">Jamshedpur - Sonari Airport (IXW)</option>
              <option value="PYB">Jeypore - Jeypore Airport (PYB)</option>
              <option value="Jhansi Airport">Jhansi Airport - Jhansi Airport</option>
              <option value="JRG">Jharsuguda Airport - Jharsuguda Airport (JRG)</option>
              <option value="VI69">Jhunjhunu Airport - Jhunjhunu Airport (VI69)</option>
              <option value="JDH">Jodhpur - Jodhpur Airport (JDH)</option>
              <option value="JRH">Jorhat - Jorhat Airport (JRH)</option>
              <option value="SLV">Jubbarhatti - Shimla Airport (SLV)</option>
              <option value="CDP">Kadapa - Kadapa Airport (CDP)</option>
              <option value="IXH">Kailashahar - Kailashahar Airport (IXH)</option>
              <option value="SAG">Kakadi - Shirdi International Airport (SAG)</option>
              <option value="GBI">Kalaburagi - Kalaburagi Airport (GBI)</option>
              <option value="IXY">Kandla - Kandla Airport (IXY)</option>
              <option value="DHM">Kangra - Kangra Airport (DHM)</option>
              <option value="Kannur">Kannur - Kannur Heliport</option>
              <option value="CNN">Kannur - Kannur International Airport (CNN)</option>
              <option value="Kanpur">Kanpur - IIT Kanpur Airport</option>
              <option value="KNU">Kanpur - Kanpur Airport (KNU)</option>
              <option value="Kanpur">Kanpur - Kanpur Civil Airport (Old)</option>
              <option value="VA1M">Karad Airport - Karad Airport (VA1M)</option>
              <option value="VI65">Kargil - Kargil Airport (VI65)</option>
              <option value="VE67">Kargong - Mechuka Advanced Landing Ground (VE67)</option>
              <option value="Karwar, Jodhpur">Karwar, Jodhpur - Fury Airport</option>
              <option value="IXK">Keshod - Keshod Airport (IXK)</option>
              <option value="HJR">Khajuraho - Khajuraho Airport (HJR)</option>
              <option value="Khandwa">Khandwa - Khandwa Airport</option>
              <option value="Khanpura">Khanpura - Gunna Ka Pura</option>
              <option value="Khargon Govt. Airstrip">Khargon Govt. Airstrip - Khargon Govt. Airstrip</option>
              <option value="IXN">Khowai - Khowai Airport (IXN)</option>
              <option value="Kishanganj">Kishanganj - Kishanganj Airport</option>
              <option value="COK">Kochi - Cochin International Airport (COK)</option>
              <option value="Kochi">Kochi - INS Garuda / Willingdon Island Naval Air Station</option>
              <option value="KLH">Kolhapur - Kolhapur Airport (KLH)</option>
              <option value="Kolkata">Kolkata - Behala Airport</option>
              <option value="CCU">Kolkata - Netaji Subhash Chandra Bose International Airport (CCU)</option>
              <option value="KTU">Kota - Kota Airport (KTU)</option>
              <option value="VI66">Koyul - Fukche Advanced Landing Ground (VI66)</option>
              <option value="KBK">Kushinagar - Kushinagar International Airport (KBK)</option>
              <option value="Lalitpur">Lalitpur - Lalitpur Airport</option>
              <option value="LTU">Latur - Murod Kond Airport (LTU)</option>
              <option value="IXL">Leh - Leh Kushok Bakula Rimpochee Airport (IXL)</option>
              <option value="IXI">Lilabari - Lilabari North Lakhimpur Airport (IXI)</option>
              <option value="Lucknow">Lucknow - Bakshi Ka Talab Air Force Station</option>
              <option value="LKO">Lucknow - Chaudhary Charan Singh International Airport (LKO)</option>
              <option value="LUH">Ludhiana Airport - Ludhiana Airport (LUH)</option>
              <option value="Madhubani">Madhubani - Madhubani Airport</option>
              <option value="RJA">Madhurapudi - Rajahmundry Airport (RJA)</option>
              <option value="IXM">Madurai - Madurai Airport (IXM)</option>
              <option value="LDA">Malda - Malda Airport (LDA)</option>
              <option value="Mamidiyal">Mamidiyal - Viraf Airstrip</option>
              <option value="Mandvi">Mandvi - Mandvi Airport</option>
              <option value="IXE">Mangaluru - Mangaluru International Airport (IXE)</option>
              <option value="IXQ">Manik Bhandar - Kamalpur Airport (IXQ)</option>
              <option value="Marhamtabad">Marhamtabad - Marhamtabad Airport</option>
              <option value="VA2B">Meerut - Dr. Bhimrao Ambedkar Airstrip (VA2B)</option>
              <option value="Mehsana">Mehsana - Mehsana Airport</option>
              <option value="Mithapur">Mithapur - Mithapur Airport</option>
              <option value="Mohammadabad">Mohammadabad - Mohammadabad Airport</option>
              <option value="GOX">Mopa - Manohar International Airport (GOX)</option>
              <option value="MZS">Moradabad - Moradabad Airport (MZS)</option>
              <option value="VA1D">Muirpur Airport - Muirpur Airport (VA1D)</option>
              <option value="BOM">Mumbai - Chhatrapati Shivaji Maharaj International Airport (BOM)</option>
              <option value="Mumbai">Mumbai - Juhu Aerodrome</option>
              <option value="Mundra">Mundra - Mundra Airport</option>
              <option value="MZU">Muzaffarpur - Muzaffarpur Airport (MZU)</option>
              <option value="MYQ">Mysore - Mysore Airport (MYQ)</option>
              <option value="Nagarjuna Sagar">Nagarjuna Sagar - Nagarjuna Sagar Airport</option>
              <option value="VI73">Nagaur Airport - Nagaur Airport (VI73)</option>
              <option value="NAG">Nagpur - Dr. Babasaheb Ambedkar International Airport (NAG)</option>
              <option value="Naliya">Naliya - Naliya Air Force Station</option>
              <option value="VO26">Nallatinputhur - Kovilpatti Airport (VO26)</option>
              <option value="NDC">Nanded - Nanded Airport (NDC)</option>
              <option value="VI20">Narnaul Airport - Narnaul Airport (VI20)</option>
              <option value="Nashik">Nashik - Gandhinagar Airfield</option>
              <option value="ISK">Nashik - Nashik International Airport (ISK)</option>
              <option value="NMI">Navi Mumbai - Navi Mumbai International Airport (NMI)</option>
              <option value="Nawapara">Nawapara - Nawapara Airport</option>
              <option value="DEL">New Delhi - Indira Gandhi International Airport (DEL)</option>
              <option value="New Delhi">New Delhi - Safdarjung Airport</option>
              <option value="NVY">Neyveli - Neyveli Airport (NVY)</option>
              <option value="VI40">Niawal - Karnal Airport (VI40)</option>
              <option value="VA1N">Nimach Airport - Nimach Airport (VA1N)</option>
              <option value="VE36">Nuagaon Airport - Nuagaon Airport (VE36)</option>
              <option value="Nubra">Nubra - Daulat Beg Oldi Advanced Landing Ground</option>
              <option value="VI57">Nubra - Thoise Airport (VI57)</option>
              <option value="Nyoma">Nyoma - Nyoma Airstrip</option>
              <option value="VA1H">Ondwa Airport - Ondwa Airport (VA1H)</option>
              <option value="KJB">Orvakal - Kurnool Airport (KJB)</option>
              <option value="Osmanabad">Osmanabad - Osmanabad Airport</option>
              <option value="PYG">Pakyong - Pakyong Airport (PYG)</option>
              <option value="Panagarh Air Force Station">Panagarh Air Force Station - Panagarh Air Force Station</option>
              <option value="PGH">Pantnagar - Pantnagar Airport (PGH)</option>
              <option value="IXT">Pasighat - Pasighat Airport (IXT)</option>
              <option value="IXP">Pathankot - Pathankot Airport (IXP)</option>
              <option value="Patiala Airport">Patiala Airport - Patiala Airport</option>
              <option value="Patna">Patna - Bihta Air Force Station</option>
              <option value="PAT">Patna - Jay Prakash Narayan Airport (PAT)</option>
              <option value="Phalodi Air Force Station">Phalodi Air Force Station - Phalodi Air Force Station</option>
              <option value="VA2A">Phalodi Airport - Phalodi Airport (VA2A)</option>
              <option value="VI70">Pilani New Airport - Pilani New Airport (VI70)</option>
              <option value="Pithoragarh">Pithoragarh - Pithoragarh Airport</option>
              <option value="Poonch">Poonch - Poonch Airport</option>
              <option value="PBD">Porbandar - Porbandar Airport (PBD)</option>
              <option value="IXZ">Port Blair - Veer Savarkar International Airport / INS Utkrosh (IXZ)</option>
              <option value="PNY">Puducherry (Pondicherry) - Pondicherry Airport (PNY)</option>
              <option value="BMT">Pune - Baramati Airport (BMT)</option>
              <option value="Pune">Pune - Hadapsar Gliding Centre</option>
              <option value="PNQ">Pune - Pune International Airport (PNQ)</option>
              <option value="Purnea Airport">Purnea Airport - Purnea Airport</option>
              <option value="PUT">Puttaparthi - Sri Sathya Sai Airport (PUT)</option>
              <option value="Rahani">Rahani - Birasal Airport</option>
              <option value="Raichur Airport">Raichur Airport - Raichur Airport</option>
              <option value="Raigarh Airport (JSPL)">Raigarh Airport (JSPL) - Raigarh Airport (JSPL)</option>
              <option value="RPR">Raipur - Swami Vivekananda Airport (RPR)</option>
              <option value="RAJ">Rajkot - Rajkot Airport (RAJ)</option>
              <option value="HSR">Rajkot - Rajkot International Airport (HSR)</option>
              <option value="RJI">Rajouri - Rajouri Airport (RJI)</option>
              <option value="RMD">Ramagundam - Basanth Nagar Airport (RMD)</option>
              <option value="Ramnad">Ramnad - Ramnad Naval Air Station</option>
              <option value="Rampurhat">Rampurhat - Surichua Air Base</option>
              <option value="IXR">Ranchi - Birsa Munda Airport (IXR)</option>
              <option value="VA2D">Ratlam Airport - Ratlam Airport (VA2D)</option>
              <option value="RTC">Ratnagiri Airport - Ratnagiri Airport (RTC)</option>
              <option value="Raxaul Airport">Raxaul Airport - Raxaul Airport</option>
              <option value="REW">Rewa - Rewa Airport, Chorhata, REWA (REW)</option>
              <option value="RRK">Rourkela - Rourkela Airport (RRK)</option>
              <option value="Rumgara">Rumgara - Korba Airport</option>
              <option value="RUP">Rupsi - Rupsi Airport (RUP)</option>
              <option value="Saharsa">Saharsa - Saharsa Airport</option>
              <option value="SXV">Salem - Salem Airport (SXV)</option>
              <option value="Sambalpur">Sambalpur - Hirakud Airport</option>
              <option value="TNI">Satna Airport - Satna Airport (TNI)</option>
              <option value="Secunderabad">Secunderabad - Hakimpet Airport</option>
              <option value="SWN">Sherpur Naqeebpur - Sarsawa Air Force Station (SWN)</option>
              <option value="SHL">Shillong - Shillong Airport (SHL)</option>
              <option value="RQY">Shimoga - Rashtrakavi Kuvempu Airport (RQY)</option>
              <option value="Shirpur">Shirpur - Shirpur Airport</option>
              <option value="VSV">Shravasti - Shravasti Airport (VSV)</option>
              <option value="VA1F">Sidhi Airport - Sidhi Airport (VA1F)</option>
              <option value="IXS">Silchar - Silchar Airport (IXS)</option>
              <option value="IXB">Siliguri - Bagdogra Airport (IXB)</option>
              <option value="VA38">Sirohi Airport - Sirohi Airport (VA38)</option>
              <option value="Sirsa Air Force Station">Sirsa Air Force Station - Sirsa Air Force Station</option>
              <option value="VE24">Sokriting T.E. - Sookerating (Doomdooma) Airport (VE24)</option>
              <option value="SSE">Solapur - Solapur Airport (SSE)</option>
              <option value="SXR">Srinagar - Srinagar International Airport (SXR)</option>
              <option value="Sultanpur">Sultanpur - Sultanpur Airport</option>
              <option value="Sulur">Sulur - Coimbatore Air Force Station</option>
              <option value="STV">Surat - Surat International Airport (STV)</option>
              <option value="VI43">Suratgarh New Airport - Suratgarh New Airport (VI43)</option>
              <option value="Tarauna">Tarauna - Fursatganj Airport</option>
              <option value="TEZ">Tezpur Airport - Tezpur Airport (TEZ)</option>
              <option value="TEI">Tezu - Tezu Airport (TEI)</option>
              <option value="TJV">Thanjavur - Thanjavur Air Force Station (TJV)</option>
              <option value="TRV">Thiruvananthapuram - Thiruvananthapuram International Airport (TRV)</option>
              <option value="VE96">Thuniabhand Airport - Thuniabhand Airport (VE96)</option>
              <option value="TRZ">Tiruchirappalli - Tiruchirappalli International Airport (TRZ)</option>
              <option value="TIR">Tirupati - Tirupati International Airport (TIR)</option>
              <option value="VDY">Toranagallu - Jindal Vijaynagar Airport (VDY)</option>
              <option value="Tuting">Tuting - Tuting Advanced Landing Ground</option>
              <option value="UDR">Udaipur - Maharana Pratap Airport (UDR)</option>
              <option value="Udhampur">Udhampur - Udhampur Air Force Station</option>
              <option value="Ujjain">Ujjain - Bentayan Airport</option>
              <option value="Umaria">Umaria - Umaria Air Field</option>
              <option value="Uttarlai Airport">Uttarlai Airport - Uttarlai Airport</option>
              <option value="BDQ">Vadodara - Vadodara International Airport (BDQ)</option>
              <option value="TCR">Vagaikulam - Tuticorin Airport (TCR)</option>
              <option value="Vanasthali">Vanasthali - Vanasthali Airport</option>
              <option value="VNS">Varanasi - Lal Bahadur Shastri International Airport (VNS)</option>
              <option value="GOI">Vasco da Gama - Goa Dabolim International Airport (GOI)</option>
              <option value="Vedanta Lanjigarh Airstrip">Vedanta Lanjigarh Airstrip - Vedanta Lanjigarh Airstrip</option>
              <option value="Vellore">Vellore - Vellore Airport</option>
              <option value="Vijay Nagar">Vijay Nagar - Vijay Nagar Airport</option>
              <option value="VGA">Vijayawada - Vijayawada International Airport (VGA)</option>
              <option value="VE91">Vijaynagar Advanced Landing Ground - Vijaynagar Advanced Landing Ground (VE91)</option>
              <option value="VTZ">Visakhapatnam - Alluri Sitarama Raju International Airport (Vizag) (VTZ)</option>
              <option value="Visakhapatnam">Visakhapatnam - INS Dega Airport (visakhapatnam international airport)</option>
              <option value="Walong Advanced Landing Ground">Walong Advanced Landing Ground - Walong Advanced Landing Ground</option>
              <option value="WGC">Warangal - Warangal Airport (WGC)</option>
              <option value="VA78">Yavatmal - Sant Gadge Baba Yavatmal Airport (VA78)</option>
              <option value="Yelahanka">Yelahanka - Yelahanka Air Force Station</option>
              <option value="ZER">Ziro - Ziro Airport (ZER)</option>
            </select>

          </div>



          {/* AIRLINE */}

          <div className="field">

            <label>

              <span>✈</span>

              Airline

            </label>

            <select id="airline">

              <option>IndiGo</option>
              <option>Air India</option>
              <option>Jet Airways</option>
              <option>SpiceJet</option>
              <option>Vistara</option>
              <option>Air Asia</option>
              <option>GoAir</option>
              <option>Kingfisher</option>

            </select>

          </div>

          




          {/* DATE */}

          <div className="field">

            <label>

              <span>◷</span>

              Journey date

            </label>

            <input
              type="date"
              id="journeyDate"
            />

          </div>



          {/* STOPS */}

          <div className="field">

            <label>

              <span>⌄</span>

              Stops

            </label>

            <select id="stops">

              <option value="0">Non-stop</option>
              <option value="1">1 Stop</option>
              <option value="2">2 Stops</option>
              <option value="3">3 Stops</option>

            </select>

          </div>



          {/* BUTTON */}

          <button
            className="predict-btn"
            id="predictBtn"
            onClick={() => window.predictFare()}
          >

            <span id="predictIcon">⚡</span>

            <span id="predictText">
              Predict fare
            </span>

          </button>

        </div>



        {/* =================================================
             RESULT
        ================================================== */}

        <div
          className="prediction-result"
          id="predictionResult"
        >

          <div className="result-header">

            <div>

              <div className="result-label">
                ESTIMATED AIRFARE
              </div>

              <div
                className="result-price"
                id="resultPrice"
              >
                ₹7,420
              </div>

              <div
                className="result-range"
                id="resultRange"
              >
                Expected range ₹6,700 – ₹8,150
              </div>

            </div>


            <div className="confidence">

              <span>✓</span>

              <strong id="confidence">
                91%
              </strong>

              <span>
                model confidence
              </span>

            </div>

          </div>


          <div className="result-route">

            <div className="result-airport">

              <strong id="resultFrom">
                DEL
              </strong>

              <span id="resultFromName">
                Delhi
              </span>

            </div>


            <div className="result-line">

              <span></span>

              <svg
                width="21"
                height="21"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
              >
                <path d="M2 16l20-8"/>
                <path d="M22 8l-6-2-5-4-2 1 3 5-7 3-3-2-1 2 4 3 7-2 4 5 2-1-2-6z"/>
              </svg>

              <span></span>

            </div>


            <div className="result-airport">

              <strong id="resultTo">
                BOM
              </strong>

              <span id="resultToName">
                Mumbai
              </span>

            </div>

          </div>
          {/* OTA SUGGESTIONS */}
          <div className="ota-suggestions" style={{ marginTop: "35px", paddingTop: "25px", borderTop: "1px solid rgba(255,255,255,0.1)" }}>
            <div className="result-label" style={{ marginBottom: "15px" }}>RECOMMENDED BOOKING OPTIONS</div>
            <div id="otaList" style={{ display: "grid", gap: "10px" }}></div>
          </div>

        </div>

      </div>

    </div>

  </section>



  {/* =======================================================
       EXPLAINABLE AI
  ======================================================== */}

  <section id="ai" className="section ai-section">

    <div className="container">

      <div className="ai-grid">


        <div className="ai-visual">

          <div className="orbit orbit-1"></div>

          <div className="orbit orbit-2"></div>

          <div className="orbit orbit-3"></div>


          <div className="ai-core">

            <svg
              width="42"
              height="42"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.6"
            >

              <circle
                cx="12"
                cy="12"
                r="3"
              />

              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6h.09A1.65 1.65 0 0 0 10 3.09V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9v.09A1.65 1.65 0 0 0 20.91 10H21a2 2 0 1 1 0 4h-.09A1.65 1.65 0 0 0 19.4 15z"/>

            </svg>

            <strong>AI</strong>

          </div>

        </div>



        <div className="ai-content">

          <div className="section-label">
            ✦ EXPLAINABLE AI
          </div>

          <h2 className="section-title">

            Not just a prediction.

            <span>Understand the price.</span>

          </h2>

          <p>

            Airlytics combines machine learning with explainable
            AI to show which flight characteristics influenced
            the predicted airfare.

          </p>


          <div className="features">


            <div className="feature">

              <div className="feature-icon">
                ↗
              </div>

              <div>

                <strong>
                  Route influence
                </strong>

                <p>
                  Understand how your source and destination
                  affect the estimated fare.
                </p>

              </div>

            </div>


            <div className="feature">

              <div className="feature-icon">
                ◷
              </div>

              <div>

                <strong>
                  Duration impact
                </strong>

                <p>
                  See how flight duration contributes to
                  the prediction.
                </p>

              </div>

            </div>


            <div className="feature">

              <div className="feature-icon">
                ▥
              </div>

              <div>

                <strong>
                  Model transparency
                </strong>

                <p>
                  Explore the factors behind every
                  Airlytics prediction.
                </p>

              </div>

            </div>


          </div>

        </div>

      </div>

    </div>

  </section>



  {/* =======================================================
       ANALYTICS
  ======================================================== */}

  <section
    id="analytics"
    className="section analytics-section"
  >

    <div className="container">

      <div className="analytics-heading">

        <div className="section-label">
          ✦ FLIGHT ANALYTICS
        </div>

        <h2 className="section-title">
          Travel intelligence at a glance
        </h2>

        <p className="section-description">

          Explore the patterns and machine-learning insights
          behind Airlytics.

        </p>

      </div>


      <div className="stats">


        <div className="stat-card">

          <div className="stat-value">
            8+
          </div>

          <h3>
            Airline categories
          </h3>

          <p>
            Multiple airline segments represented in the
            airfare dataset.
          </p>

        </div>


        <div className="stat-card">

          <div className="stat-value">
            450+
          </div>

          <h3>
            Indian Airports
          </h3>

          <p>
            Comprehensive coverage of large, medium, and small airports across India.
          </p>

        </div>


        <div className="stat-card">

          <div className="stat-value">
            20+
          </div>

          <h3>
            Booking Platforms
          </h3>

          <p>
            Real-time price intelligence across major Indian OTAs and direct airlines.
          </p>

        </div>


        <div className="stat-card">

          <div className="stat-value">
            90.19%
          </div>

          <h3>
            AI Accuracy (R²)
          </h3>

          <p>
            Highly confident airfare prediction powered by Random Forest ML.
          </p>

        </div>


      </div>

    </div>

  </section>



  {/* =======================================================
       ROUTE EXPLORER
  ======================================================== */}

  <section className="section routes-section">

    <div className="container">

      <div className="routes-header">

        <div>

          <div className="section-label">
            ✦ ROUTE EXPLORER
          </div>

          <h2 className="section-title">
            Explore popular routes
          </h2>

        </div>


        <button className="outline-button">

          View all routes

          →

        </button>

      </div>


      <div className="routes-grid">


        <div className="route-card">

          <div className="route-airports">

            <strong className="route-code">
              DEL
            </strong>

            <div className="mini-route">
              <span></span>
              ✈
              <span></span>
            </div>

            <strong className="route-code">
              BOM
            </strong>

          </div>

          <div className="route-bottom">

            <small>
              Estimated fare
            </small>

            <strong className="route-price">
              ₹7,420
            </strong>

          </div>

        </div>



        <div className="route-card">

          <div className="route-airports">

            <strong className="route-code">
              DEL
            </strong>

            <div className="mini-route">
              <span></span>
              ✈
              <span></span>
            </div>

            <strong className="route-code">
              BLR
            </strong>

          </div>

          <div className="route-bottom">

            <small>
              Estimated fare
            </small>

            <strong className="route-price">
              ₹8,120
            </strong>

          </div>

        </div>



        <div className="route-card">

          <div className="route-airports">

            <strong className="route-code">
              CCU
            </strong>

            <div className="mini-route">
              <span></span>
              ✈
              <span></span>
            </div>

            <strong className="route-code">
              DEL
            </strong>

          </div>

          <div className="route-bottom">

            <small>
              Estimated fare
            </small>

            <strong className="route-price">
              ₹6,840
            </strong>

          </div>

        </div>



        <div className="route-card">

          <div className="route-airports">

            <strong className="route-code">
              BOM
            </strong>

            <div className="mini-route">
              <span></span>
              ✈
              <span></span>
            </div>

            <strong className="route-code">
              COK
            </strong>

          </div>

          <div className="route-bottom">

            <small>
              Estimated fare
            </small>

            <strong className="route-price">
              ₹5,970
            </strong>

          </div>

        </div>


      </div>

    </div>

  </section>



  {/* =======================================================
       MODEL PERFORMANCE
  ======================================================== */}

  <section
    id="model"
    className="section model-section"
  >

    <div className="container">

      <div className="model-card">

        <div>

          <div className="section-label">
            ✦ MACHINE LEARNING
          </div>

          <h2 className="section-title">

            Built on a validated
            <span className="blue">
              ML pipeline.
            </span>

          </h2>

          <p className="section-description">

            Airlytics combines data preprocessing,
            feature engineering, model selection,
            cross-validation and explainable AI.

          </p>

        </div>


        <div className="model-metrics">


          <div className="metric">

            <span>
              R²
            </span>

            <strong>
              0.9019
            </strong>

          </div>


          <div className="metric">

            <span>
              MAE
            </span>

            <strong>
              640.33
            </strong>

          </div>


          <div className="metric">

            <span>
              RMSE
            </span>

            <strong>
              1430.08
            </strong>

          </div>


        </div>

      </div>

    </div>

  </section>



  {/* =======================================================
       FOOTER
  ======================================================== */}

  <footer>

    <div className="footer-brand">

      <div className="logo-icon">

        <svg
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M2 16l20-8"/>
          <path d="M22 8l-6-2-5-4-2 1 3 5-7 3-3-2-1 2 4 3 7-2 4 5 2-1-2-6z"/>
        </svg>

      </div>


      <div className="footer-brand-text">

        <strong>
          Airlytics
        </strong>

        <span>
          Intelligent Airfare Analytics
        </span>

      </div>

    </div>


    <div className="footer-description">

      Machine-learning powered flight intelligence.

    </div>

  </footer>



  {/* =======================================================
       JAVASCRIPT
  ======================================================== */}

  


    </div>
  );
}
