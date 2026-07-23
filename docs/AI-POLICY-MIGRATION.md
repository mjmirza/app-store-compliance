<!-- AI_POLICY_MONITOR_START -->
# AI Policy Monitoring & Compliance Report

This report is continuously generated and updated by `scripts/monitor.py` to keep track of platform policy changes.

## Latest Monitored Policy Changes

### Build intelligent Android apps: Cloud and hybrid inference (Google Play)
- **Published**: 2026-07-21T09:58:09.514-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html](https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html)
- **Key Topics**: AI-generated content disclosures, User safety requirements
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiBHTpa22SxEltoebLZYO_34iRtahN8z5tA3tnIryIii0s4_conN5qFYfmNro6nmZBfsgiZeRLtru-gE4XO2mf-RBDyIo00kf3QunWwUO-SICHkVSv0exAQQ4qA0KzjMGRpA8qj1TSMP0Ffe0FzrEc_S1zBaakKzCZFpqYLXqds9Zqmqr8yyeSgyNl9U0s/s2469/features%20in%20Jetpacker%20Features%20with%20Firebase%20AI%20Logic%20_Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiBHTpa22SxEltoebLZYO_34iRtahN8z5tA3tnIryIii0s4_conN5qFYfmNro6nmZBfsgiZeRLtru-gE4XO2mf-RBDyIo00kf3QunWwUO-SICHkVSv0exAQQ4qA0KzjMGRpA8qj1TSMP0Ffe0FzrEc_S1zBaakKzCZFpqYLXqds9Zqmqr8yyeSgyNl9U0s/s2469/features%20in%20Jetpacker%20Features%20with%20Firebase%20AI%20Logic%20_Meta.png" style="display: none;" /><div><i>Posted by Thomas Ezan, Jolanda Verhoef, Caren Chang, Senior Developer Relations Engineers, Android Developer Relations</i></div><div><br /></div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjn2fO3T2xckksQ9pk3RUNPxZqqq2CyaifXnju0lCCpbfwJ4gZyq-df0kM_mK1TMV0F9YCMo19Ba9NvFAiUpzDH6Wlk_RyonRCK5Ono25CYyQ7xGC3q70mUhyphenhyphenOOYJ-5JX2KlFP1lIA3ULIhH86_hP2ptO0AllUIf6ZVh-SqoXVWcXrM8m3hHCkhGwZYfP4/s8583/AFD%20-%20%5BABL_101%5D%20Building%20AI%20features%20in%20Jetpacker%20Features%20with%20Firebase%20AI%20Logic%20_Blog.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2601" data-original-width="8583" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjn2fO3T2xckksQ9pk3RUNPxZqqq2CyaifXnju0lCCpbfwJ4gZyq-df0kM_mK1TMV0F9YCMo19Ba9NvFAiUpzDH6Wlk_RyonRCK5Ono25CYyQ7xGC3q70mUhyphenhyphenOOYJ-5JX2KlFP1lIA3ULIhH86_hP2ptO0AllUIf6ZVh-SqoXVWcXrM8m3hHCkhGwZYfP4/s1600/AFD%20-%20%5BABL_101%5D%20Building%20AI%20features%20in%20Jetpacker%20Features%20with%20Firebase%20AI%20Logic%20_Blog.png" /></a></div><br /><p><br /></p><p>Welcome back to the blog post series "<a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html" target="_blank">Build intelligent Android apps</a>" where we take a basic Android app and transform it into a <b>personalized</b>, <b>intelligent</b>, and <b>agentic</b> experience. In our <a href="http://android-developers.googleblog.com/2026/07/android-on-device-inference.html">previous post</a> we explored how to build intelligent on-device features using Gemini Nano through ML Kit's Prompt API.</p>

<p>In this post, we will look at how you can leverage <b><a href="https://firebase.google.com/docs/ai-logic">Firebase AI Logic</a> </b>to build cloud-hosted and hybrid AI features:&nbsp;</p>
<ul>
  <li>Grounding answers in real-world context</li>
  <li>Routing requests dynamically between cloud and local execution using hybrid inference</li>
  <li>Translating content with custom routing systems</li>
</ul>

<div style="margin: 0px auto; width: 100%;">
  <iframe allowfullscreen="" src="https://www.youtube.com/embed/_iuXykdlTkk" style="aspect-ratio: 16/9; border: 0; width: 100%;">
  </iframe>
</div><p><br /></p><p>Sometimes a use case requires AI models with greater world knowledge, a much larger context window, or the ability to handle complex queries. In those scenarios, we can leverage cloud models.&nbsp;</p>

<p>Other times, you want the best of both worlds: using hybrid inference to run on-device when available to lower costs, while falling back to the cloud to ensure compatibility for all devices.</p><br /><div class="separator" style="clear: both; text-align: center;"><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhwlTUF1Kzkbrf2w64KO3jZJZZ_wLEu34vq6Cb7PX2alVUhFVdbkiWuXCkzUS-bPJkHMbmuNJ_Ov0HYZzujr69jCU9gPvmKaKMZt2q4-TolSDFCLABBIY1IBRY9Zn7D5S10hFcJD2kuVCm3N2glpqDJoHiqAZat4z6oyXxxwH4ZCGVBgfPObMevoJrgNPg/s8000/features_upscaled.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="4744" data-original-width="8000" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhwlTUF1Kzkbrf2w64KO3jZJZZ_wLEu34vq6Cb7PX2alVUhFVdbkiWuXCkzUS-bPJkHMbmuNJ_Ov0HYZzujr69jCU9gPvmKaKMZt2q4-TolSDFCLABBIY1IBRY9Zn7D5S10hFcJD2kuVCm3N2glpqDJoHiqAZat4z6oyXxxwH4ZCGVBgfPObMevoJrgNPg/s1600/features_upscaled.png" /></a></div><em style="text-align: left;">Cloud and hybrid features in Jetpacker: Museum assistant with web grounding, hybrid restaurant review drafting, and&nbsp;
  support chat featuring custom-routed live translation.</em></div>

<p>Let’s look at how we implemented three cloud and hybrid features in <a href="https://github.com/android/ai-samples/tree/main/jetpacker" target="_blank">Jetpacker</a>:</p>
<ul>
  <li>a museum assistant with web grounding</li>
  <li>hybrid restaurant review drafting</li>
  <li>hotel support chat featuring custom-routed live translation.</li>
</ul>

<h2>Use LLM grounding for up-to-date informationMuseum assistant chatbot with LLM grounding</h2>
<p>The <b>Museum assistant </b>is an interactive chatbot designed to help users plan their museum visits. It provides visitors with up-to-date details regarding specific exhibits, current opening hours, ticket pricing, and more.</p><br /><div class="separator" style="clear: both; text-align: center;"><em style="text-align: left;"><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj3pxeCVJfOo5G7McNB4RCIhoCUch8CHSAWI7gHijJJcE95b0gbu3lyAO1xIWc6mKllkpylSPBnVfU6RYnwfay4z6dH7TlufPuNw3Lw7s-bEuR4Ajx8IHK8k6zJcOHitqMRdDv8EVL-fCN6uuDo1QTnOgk_RW-AEM1_hZaJWbCGezMQF_D9Hia-Rm2T4-c/s4880/museum_assistant_upscaled.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="4880" data-original-width="2392" height="640" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj3pxeCVJfOo5G7McNB4RCIhoCUch8CHSAWI7gHijJJcE95b0gbu3lyAO1xIWc6mKllkpylSPBnVfU6RYnwfay4z6dH7TlufPuNw3Lw7s-bEuR4Ajx8IHK8k6zJcOHitqMRdDv8EVL-fCN6uuDo1QTnOgk_RW-AEM1_hZaJWbCGezMQF_D9Hia-Rm2T4-c/w314-h640/museum_assistant_upscaled.png" width="314" /></a></div>Museum assistant is a chatbot that answers questions, such as&nbsp;</em></div><div class="separator" style="clear: both; text-align: center;"><em style="text-align: left;">‘How can I get a ticket discount for Le Louvre?’</em></div>

<p>When building AI features, getting the model to answer with fresh, accurate, and specific real-world information is a common challenge. While cloud models possess massive amounts of world knowledge, they might not know about seasonal exhibits or the current day’s opening hours.&nbsp;</p><div class="separator" style="clear: both; text-align: center;"><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi8He5M2JC5EwXZwa-M52UAXHSO4dWy4gx3aZoY2ZXM-x25pV4kc6BsICe_fG4Zn6-R37_UgTQ8LBSsrNcP50e3aQLgxNbHOfWLBqzaSqQ78ZDmNEJadZNc-I5bduHr0UtWOxYMTFAHgffxcuzaETHPe3lvfRod2rkeOUXnRaLJ_vIiAfO_xRKpESbX3L8/s8000/grounding_upscaled.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="4452" data-original-width="8000" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi8He5M2JC5EwXZwa-M52UAXHSO4dWy4gx3aZoY2ZXM-x25pV4kc6BsICe_fG4Zn6-R37_UgTQ8LBSsrNcP50e3aQLgxNbHOfWLBqzaSqQ78ZDmNEJadZNc-I5bduHr0UtWOxYMTFAHgffxcuzaETHPe3lvfRod2rkeOUXnRaLJ_vIiAfO_xRKpESbX3L8/s1600/grounding_upscaled.png" /></a></div><br /><em style="text-align: left;"><br />Grounding data is added to the context window to enable the model</em></div><div class="separator" style="clear: both; text-align: center;"><em style="text-align: left;">&nbsp;to answer questions correctly and accurately.</em></div>

<p>To bridge this gap, we can use grounding techniques to add extra context to the model’s context window. The <a href="https://firebase.google.com/products/firebase-ai-logic" target="_blank">Firebase AI Logic SDK</a> supports three types of grounding:</p>
<ul>
  <li><strong><a href="https://firebase.google.com/docs/ai-logic/url-context">URL grounding</a>:</strong> Grounding responses using content from a specific webpage (e.g. current ticket prices or museum rules).</li>
  <li><strong><a href="https://firebase.google.com/docs/ai-logic/grounding-google-search">Google Search grounding</a>:</strong> Letting the model query the real-time Google search index for up-to-date details.</li>
  <li><strong><a href="https://firebase.google.com/docs/ai-logic/grounding-google-maps">Maps grounding</a>:</strong> Using Google Maps location data.</li>
</ul>

<p>In Jetpacker, we dynamically construct the available tools based on enabled feature flags and initialize the generative model using the Firebase AI SDK:</p>

<pre><code>// implementation("com.google.firebase:firebase-ai-logic")

private var toolList = mutableListOf&lt;Tool&gt;()

init {
    if (ENABLE_SEARCH_GROUNDING) {
        toolList.add(Tool.googleSearch())
    }
    if (ENABLE_URL_GROUNDING) {
        toolList.add(Tool.urlContext())
    }
}

private val generativeModel = Firebase.ai(backend = GenerativeBackend.googleAI())
    .generativeModel(
        modelName = "gemini-3-flash",
        systemInstruction = content {
            text("You are a helpful museum assistant answering questions about a museum. Use plain text.")
        },
        tools = toolList
    )</code></pre>

<p>When the user queries the assistant, if URL grounding is enabled, we append the specific museum resource URLs directly into the prompt:</p>

<pre><code>val groundingText = if (FeatureFlags.ENABLE_URL_GROUNDING) {
    "\n If the following message above is about the rules and terms to visit Le Louvre, " +
    "if needed answer this urls ${urlList.joinToString()}"
} else {
    ""
}

val prompt = "$text $groundingText"

var response = chat.sendMessage(prompt)
</code></pre>

<h2>Hybrid inference: On-device review generation with Maps deep link</h2>
<p>Not every AI task requires a cloud-based model, and not every device is online. To help developers balance latency, cost, and offline availability, we recently introduced the <a href="https://firebase.google.com/docs/ai-logic/hybrid/android/get-started?api=dev">Firebase API for Hybrid Inference</a>.</p>

<p>In Jetpacker, the <b>restaurant review</b> feature lets users review select topics and automatically drafts a review. To enable this for all users, we prioritize local execution with Gemini Nano, and fall back to cloud models on devices that don’t support Gemini Nano.&nbsp;</p><div class="separator" style="clear: both; text-align: center;"><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjVa1o2Zh3v3Babi7gGmzOFYAKPEgS0HWmvisiKgK-QsSRh_ZhjTjuUYSS_QIH0JQw9NsqrkYe4Quud6cfCGwVc61_7HKcACj6c9yywWySn5xyHGgemBR5tYPP8q3bmLadaN6uLXspE9LqrcZkVdckEGHWDhdfYVa-xo8QomDaRn03mau2fHVyK0Fr1FaU/s4680/review_upscaled.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="4680" data-original-width="2392" height="640" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjVa1o2Zh3v3Babi7gGmzOFYAKPEgS0HWmvisiKgK-QsSRh_ZhjTjuUYSS_QIH0JQw9NsqrkYe4Quud6cfCGwVc61_7HKcACj6c9yywWySn5xyHGgemBR5tYPP8q3bmLadaN6uLXspE9LqrcZkVdckEGHWDhdfYVa-xo8QomDaRn03mau2fHVyK0Fr1FaU/w327-h640/review_upscaled.png" width="327" /></a></div><br /></div><div class="separator" style="clear: both; text-align: center;"><em>The restaurant review feature uses hybrid inference to draft a review based on topics</em></div><div class="separator" style="clear: both; text-align: center;"><em><br /></em></div>

<pre><code>// implementation("com.google.firebase:firebase-ai-logic")
// implementation("com.google.firebase:firebase-ai-ondevice:16.0.0-beta03")


// Initialize the model with hybrid routing configuration
val reviewModel = Firebase.ai.generativeModel(
    modelName = "gemini-3.1-flash-lite",
    onDeviceConfig = OnDeviceConfig(
        inferenceMode = InferenceMode.PREFER_ON_DEVICE
    )
)</code></pre>

<p>The Hybrid Inference API supports four distinct routing modes:</p>
<ul>
  <li><strong>PREFER_ON_DEVICE:</strong> Prioritizes local execution and falls back to cloud if Gemini Nano is unavailable.</li>
  <li><strong>PREFER_IN_CLOUD:</strong> Prioritizes cloud execution and falls back to on-device if the device goes offline.</li>
  <li><strong>ONLY_ON_DEVICE:</strong> Restricts execution strictly to the device.</li>
  <li><strong>ONLY_IN_CLOUD:</strong> Restricts execution strictly to the cloud.</li>
</ul>

<p>Once the review is generated, we copy it to the clipboard and use an intent to open Google Maps directly to the restaurant's review page, providing a seamless user experience:</p>

<pre><code>private fun copyAndOpenMapsReview(context: Context, reviewText: String, placeId: String) {
    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    val clip = ClipData.newPlainText("User Review", reviewText)
    clipboard.setPrimaryClip(clip)

    val uri = Uri.parse("https://search.google.com/local/writereview/mobile?placeid=$placeId")
    val intent = Intent(Intent.ACTION_VIEW, uri).apply {
        setPackage("com.google.android.apps.maps")
    }
    context.startActivity(intent)
}</code></pre>

<h2>Custom hybrid routing: Hotel support chat translation with simulated personas</h2>
<p>The <b>hotel support chat</b> was built to let users finalize logistics and check on hotel details. This feature uses system instructions to configure a localized receptionist assistant. By passing specific information—such as the preferred language and hotel information—in the instructions, we can set up a conversational persona representing a specific hotel.</p>

<pre><code>private val generativeModel = Firebase.ai(backend = GenerativeBackend.googleAI())
    .generativeModel(
        systemInstruction = content {
            text("""
              You are a helpful hotel receptionist at $hotelName only speaking $language.
              Answer politely in $language. The bar closes at 10pm and breakfast is from 7am to 10am.
              There's someone at the desk 24/7. You can retrieve your luggage from the storage room
              at the back of the lobby at any time.
              """)
        },
        modelName = "gemini-3-flash-preview"
    )</code></pre>

<p>Because receptionist responses are in the hotel's local language (for example, French for Hotel Le Meurice in Paris), we need to translate messages to the user’s preferred language.&nbsp;</p><div class="separator" style="clear: both; text-align: center;"><em><br /><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEikIB_NnUYK8GnEpI3foNLO2_AQ2lNZhoc9gFB-CjERDjMwrdQ2T45y6jzrJAafi4Jz7eF_SBkXG7csDwpajKctp5yo1hsBjIacIfK3aHvvQjCUu22qZBj7dLl5Q4aGFJRD4hwTlMMNgZD8sIuYpCrRjMmpa5ybXDzi9nkTMZoiJOEn8jLmqBsgTXcVTDY/s4112/translation_upscaled.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2364" data-original-width="4112" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEikIB_NnUYK8GnEpI3foNLO2_AQ2lNZhoc9gFB-CjERDjMwrdQ2T45y6jzrJAafi4Jz7eF_SBkXG7csDwpajKctp5yo1hsBjIacIfK3aHvvQjCUu22qZBj7dLl5Q4aGFJRD4hwTlMMNgZD8sIuYpCrRjMmpa5ybXDzi9nkTMZoiJOEn8jLmqBsgTXcVTDY/s1600/translation_upscaled.png" /></a></div><div class="separator" style="clear: both; text-align: center;"><em>Hotel support chat messages are automatically translated to the user’s preferred language&nbsp;</em></div></em></div>

<p>While hybrid models can configure simple routing preferences, complex scenarios require custom routing logic. In Jetpacker, we implement a custom routing stack that takes into account:</p>
<ul>
  <li><strong>Language identification:</strong> Using the on-device <a href="https://developers.google.com/ml-kit/language/identification/android">ML Kit Language Identification API</a>, we can detect the incoming message language.</li>
  <li><strong>On-device translation (Gemini Nano):</strong> <a href="https://developers.google.com/ml-kit/genai/prompt/android">ML Kit’s Prompt API</a> lets us translate common language pairs directly on the device, saving bandwidth and cloud cost.</li>
  <li><strong>Cloud translation (Gemini 3 Flash):</strong> For more complex languages, we use Gemini Flash 3 to get a higher quality translation.</li>
</ul>

<pre><code>// implementation("com.google.android.gms:play-services-mlkit-language-id:17.0.0")&nbsp;

// ML Kit for Language Identification (powered by Google Play Services)
private val languageIdentifier = LanguageIdentification.getClient()

// On-device translator model (prefer Gemini Nano) for translating common language pairs
private val hybridTranslationModel = Firebase.ai(backend = GenerativeBackend.googleAI())
    .generativeModel(
        modelName = "gemini-3-flash",
        onDeviceConfig = OnDeviceConfig(mode = InferenceMode.PREFER_ON_DEVICE)
    )

// Cloud translator model for more complex language pairs
private val cloudTranslationModel = Firebase.ai(backend = GenerativeBackend.googleAI())
    .generativeModel(
        modelName = "gemini-3-flash"
    )</code></pre>

<p>When a message needs to be translated, we identify the source language and apply our custom routing logic, executing either on-device or cloud translation:</p>

<pre><code>fun translateMessage(message: SupportChatMessage) {
    viewModelScope.launch {
        // 1. Detect language using ML Kit Language Identification
        val sourceLang = try {
            Tasks.await(languageIdentifier.identifyLanguage(message.text))
        } catch (e: Exception) {
            "Undefined"
        }

        // 2. Custom routing: we've verified the translation quality for English and Korean with Gemini Nano, and will translate message on-device for those two languages
        val routeToCloud = sourceLang != "en" &amp;&amp; sourceLang != "kr"

        val prompt = "Translate the following text to $selectedLanguage. Just return the translated sentence: ${message.text}."

        val (translatedText, routePrefix) = if (routeToCloud) {
            val result = cloudTranslationModel.generateContent(prompt)
            result.text to "[Cloud]"
        } else {
            val result = hybridTranslationModel.generateContent(prompt)
            result.text to "[On-Device]"
        }

        if (translatedText != null) {
            _translations.update { current -&gt;
                current + (message.id to "$routePrefix: $translatedText")
            }
        }
    }
}</code></pre>

<p>In this example, the custom routing logic only takes into consideration the translation’s source and target language. However, based on your app’s use case, you can expand the routing logic to include other factors such as the on-device model version, network connectivity, battery status, and more.</p>

<h2>Securing the AI Pipelines: Firebase App Check</h2>
<p>Lastly, using AI in the cloud opens up possibilities of API key abuse or unauthorized billing. To secure API calls, we integrated <a href="https://firebase.google.com/docs/app-check"><b>Firebase App Check</b></a> using both Play Integrity (production) and the local Debug Provider (for local development or emulators).</p>

<p>In the <a href="https://github.com/android/ai-samples/blob/main/jetpacker/android/app/src/main/kotlin/com/example/jetpacker/JetPackerApplication.kt">JetPackerApplication.kt</a> file, we install the debug provider at startup and trigger anonymous authentication to establish a secure user session:</p>

<pre><code>//  implementation("com.google.firebase:firebase-appcheck-playintegrity")&nbsp;
//  implementation("com.google.firebase:firebase-appcheck-debug")&nbsp;&nbsp;
//  implementation("com.google.firebase:firebase-auth")&nbsp;

override fun onCreate() {
    super.onCreate()
    Firebase.initialize(context = this)
    Firebase.appCheck.installAppCheckProviderFactory(
        DebugAppCheckProviderFactory.getInstance()
    )
    Firebase.auth.signInAnonymously()
}</code></pre>

<p>When building locally on an emulator, App Check prints a local token secret to logcat:</p>

<p>Enter this debug secret into the allow list in the Firebase Console: a8c2dd4c-xxxx-xxxx-xxxx-ef6c114ba27e</p>

<p>Once registered in the Firebase console, local requests are fully verified and authenticated by App Check, protecting our backend while letting us test the app locally.</p>

<h2>Conclusion</h2>
<p>By combining cloud model capabilities (grounding, system instructions) with on-device capabilities (hybrid routing, translation, security app checks), we created a travel app that is smart, secure, and available offline.</p>

<p>Check out the <a href="https://github.com/android/ai-samples/tree/main/jetpacker" target="_blank">full source code for Jetpacker on GitHub</a>, and explore the Firebase documentation to get started:</p>
<p><a href="https://firebase.google.com/docs/ai-logic/get-started">Firebase AI Logic Documentation</a><br /><a href="https://firebase.google.com/docs/ai-logic/hybrid/android/get-started">Firebase Hybrid Inference API</a></p>

<h2>Learn more</h2>
<p>Check out the other parts of this blog post series:</p>
<p><b><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html">Part 1</a>:</b> Introduction of the app and a high-level overview.<br /><b><a href="http://android-developers.googleblog.com/2026/07/android-on-device-inference.html">Part 2</a>: </b>On-device intelligence. Deep-dive into ML Kit’s GenAI APIs and Gemini Nano to build privacy-first features like itinerary summarization, receipt parsing, and local audio processing.<br /><b><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html">Part 3 (this post!):</a></b> Hybrid and cloud reasoning. Explore how to use Firebase AI Logic to ground LLM answers in real-world data like Google Maps and web context.<br /><b><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-appfunctions.html">Part 4:</a> </b>System integration. Integrating with the Android intelligence system using AppFunctions.&nbsp;<br /><b>Part 5 (coming soon):</b> In-app agentic workflows. Extend the app with an end-to-end booking assistant powered by A2UI and ADK.</p>

<p>Interested in more on Android Development? Follow Android Developers on <a href="https://www.youtube.com/@AndroidDevelopers">YouTube</a> or <a href="https://www.linkedin.com/showcase/androiddev/">LinkedIn</a>!</p>

<p>All code snippets in this blog post follow the following copyright notice:</p>
<pre><code>Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0</code></pre>

### Build intelligent Android apps: Integrate into Android's intelligence system using AppFunctions (Google Play)
- **Published**: 2026-07-21T10:11:16.439-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-appfunctions.html](https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-appfunctions.html)
- **Key Topics**: User safety requirements
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi961epgT3N_Za_k2-pCJ30tegn7DM-Umh1LWh7Q4NxhryR5H57JB00zKQcek56ccAvEM95i6wyXWWCZZ7486_Gq1ewxPHtsMY13UVsVTmndAvkOJtHPjUXuZ3XW_yBEFtlOr2ocBFIKr0PCRZhIRs67h6bX6zDKihwcxQs8bGbYTqIp5azuBKcX4PNMMY/s2469/AFD%20-%20%5BABL_104%5D%20JetPacker%20AppFunctions_Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi961epgT3N_Za_k2-pCJ30tegn7DM-Umh1LWh7Q4NxhryR5H57JB00zKQcek56ccAvEM95i6wyXWWCZZ7486_Gq1ewxPHtsMY13UVsVTmndAvkOJtHPjUXuZ3XW_yBEFtlOr2ocBFIKr0PCRZhIRs67h6bX6zDKihwcxQs8bGbYTqIp5azuBKcX4PNMMY/s2469/AFD%20-%20%5BABL_104%5D%20JetPacker%20AppFunctions_Meta.png" style="display: none;" /><p></p><p><i>Posted by Ben Weiss, Senior Developer Relations Engineer,&nbsp;Android Developer Relations</i></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi92OFxAOxVMpResmBcBoUfxzgcMmVOMn3mXQabB9O-xkC7pjYxrvXS7YLTEWLIBstwuDLc0ePCC-Tf7AKq62mgAXjSYg9-VUIjKvokK6BhGHqPDSXCTQowbpj40plsP3V3Ju3ck4gzNdJmGQ6C1-twuob2UnPu7oY9B_oSwnYSkaif7lSEMwFnStzWknM/s8583/AFD%20-%20%5BABL_104%5D%20JetPacker%20AppFunctions_Blog.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2601" data-original-width="8583" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi92OFxAOxVMpResmBcBoUfxzgcMmVOMn3mXQabB9O-xkC7pjYxrvXS7YLTEWLIBstwuDLc0ePCC-Tf7AKq62mgAXjSYg9-VUIjKvokK6BhGHqPDSXCTQowbpj40plsP3V3Ju3ck4gzNdJmGQ6C1-twuob2UnPu7oY9B_oSwnYSkaif7lSEMwFnStzWknM/s1600/AFD%20-%20%5BABL_104%5D%20JetPacker%20AppFunctions_Blog.png" /></a></div><br /><p><br /></p><p>Welcome back to the blog post series "<a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html" target="_blank">Build intelligent Android apps</a>" where we take a basic Android app and transform it into a personalized, intelligent, and agentic experience. In our <a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html">previous post</a>,&nbsp;we explored how to leverage Firebase AI Logic to build cloud-hosted and hybrid AI features.</p>Traditional mobile UIs excel at focused, hands-on tasks, and the Android intelligence system is introducing complementary features to make complex, multi-step actions even easier. By supplementing traditional user interfaces, AppFunctions provide a powerful new entry point: A privileged agent on the device can access app features in the background. This can be particularly helpful when users are driving, walking or otherwise multitasking.

<p>In this article, we'll show you how we designed and integrated these capabilities into our travel planning app, <a href="https://github.com/android/jetpacker">JetPacker</a>, using Android AppFunctions. We'll explore the rationale behind our feature choices, discuss the specialized tooling we used to accelerate development, and dive into the code that makes it all work.</p>

<h2>Designing AI-ready features: making choices that matter for your users</h2>

<p>To select which features to provide to the intelligence system, we looked for tasks where a voice or text command is objectively faster than tapping through screens. In this side-by-side screen recording you can see this contrast perfectly: on the left, a user tapping through multiple screens to log an expense; on the right, the same task completed instantly in the background via a privileged agent.</p>

<div class="vertical-video-grid">
  <div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiIr2ssY2GiOlBmFzcP-91j91VjH9QX_sOP8FcmtirYPyXZmYRzNJmfqI_GT6aXYXye8-ntylv-gTNu1Qlnbx5gHiFn9naHqt7tJOQBA3HpQ5uz8XRdavXh7b3IP3FzJb4SsbC4mClGLUHupDwIeE9Du3PNRQr0SGs2lgHZTdHXnv8TagNBRtoJsbpeE6c/s960/Comp%201.gif" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="540" data-original-width="960" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiIr2ssY2GiOlBmFzcP-91j91VjH9QX_sOP8FcmtirYPyXZmYRzNJmfqI_GT6aXYXye8-ntylv-gTNu1Qlnbx5gHiFn9naHqt7tJOQBA3HpQ5uz8XRdavXh7b3IP3FzJb4SsbC4mClGLUHupDwIeE9Du3PNRQr0SGs2lgHZTdHXnv8TagNBRtoJsbpeE6c/s1600/Comp%201.gif" /></a></div><br /><div class="vertical-video-wrapper"><br /></div>

<p>Our first choice was expense tracking. Logging a coffee expense during a trip usually takes quite a few taps—unlocking the phone, opening the app, finding the active trip, navigating to the expenses tab, tapping the add button, taking a picture of the receipt, and checking the result. By providing the <code>addExpense</code> and <code>getExpenses</code> features as AppFunctions, the system agent handles the heavy lifting. When the user says, "Add a five-dollar coffee expense to my Paris trip," the agent automatically searches for the correct trip ID in the background and inserts the expense, skipping the manual UI flow entirely.</p>

<p>We also prioritized itinerary management. Finding what activity is next on a busy trip itinerary usually requires scrolling through a dense timeline view. By providing <code>getItinerary</code> and <code>addItineraryEvent</code> to the system, the user can simply ask, "What am I doing next in Paris?" and get an immediate answer.</p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiRduisOXPFs0o2m-JwtESU1fUEanqH-A0eGt58MUuXs-vgN1af77M-j3ETdegzulBq-3TClrDvhO2K_8q4ep8xAlnW1y5T09ZxxHyZmTRtftA9DOmIk7ykfM_JihQ2c2fcUbEA-jCO1sgW2JnxN9qtB8IS58lbQoaIk4cPJPuPQavZNUoW2rNKo9r8g9M/s960/Comp%202.gif" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="540" data-original-width="960" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiRduisOXPFs0o2m-JwtESU1fUEanqH-A0eGt58MUuXs-vgN1af77M-j3ETdegzulBq-3TClrDvhO2K_8q4ep8xAlnW1y5T09ZxxHyZmTRtftA9DOmIk7ykfM_JihQ2c2fcUbEA-jCO1sgW2JnxN9qtB8IS58lbQoaIk4cPJPuPQavZNUoW2rNKo9r8g9M/s1600/Comp%202.gif" /></a></div><br /><p><br /></p>


<p>Finally, we focused on hands-free note capturing. Typing out reminders or notes while walking down a busy street is difficult and unsafe. Exposing a voice note capability allows the user to say, "The flight was amazing, I saw a beautiful sunset and managed to sleep well," and the privileged agent automatically transcribes and saves it directly into the travel database&nbsp;<span face="Roboto, sans-serif" style="color: #073042; font-size: 11pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">&nbsp;using the </span><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 11pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">addVoiceNote</span><span face="Roboto, sans-serif" style="color: #073042; font-size: 11pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;"> AppFunction.</span></p>

<h2>Android MCP powered by AppFunctions</h2>This entire experience is built on Android MCP. Under this design, the app acts as a local MCP server. Rather than remote APIs, you provide your app features directly to the on-device intelligence system.<br /><br /><a href="https://d.android.com/ai/appfunctions">Android AppFunctions</a> is the API that brings this concept to life. It reads annotated Kotlin functions and compiles them into type-safe, sandboxed tool definitions that the privileged agent can discover and invoke locally on the device.<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjypEvh8lAK1myAWpnG4A0TtdIaTxP69t7g9croAJSUZ2Od6AEkhwMusN3CvdGohdvYzoh1UaCxCHb22oJzCD_4B2K8vfQzcyAIaTl8lk3TCR9T0SoMHjjaDk4GMxxPazeCfT0aF7rifm7-LAvcMhyphenhyphenryDJpOPYon7jiISKB2sMLzAwHDuKFxIv16sDXjrM/s2500/Android%20MCP%20diagram.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1406" data-original-width="2500" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjypEvh8lAK1myAWpnG4A0TtdIaTxP69t7g9croAJSUZ2Od6AEkhwMusN3CvdGohdvYzoh1UaCxCHb22oJzCD_4B2K8vfQzcyAIaTl8lk3TCR9T0SoMHjjaDk4GMxxPazeCfT0aF7rifm7-LAvcMhyphenhyphenryDJpOPYon7jiISKB2sMLzAwHDuKFxIv16sDXjrM/s1600/Android%20MCP%20diagram.png" /></a></div><br /><p><br /></p>

<p><br /></p><p><br /></p><p><br /></p><p><br /></p><p><br /></p><i><div style="text-align: center;"><i>Diagram highlighting our apps, the android platform, and system agents coordinate AppFunctions.</i></div></i><p>Under the Android MCP model, your app acts as a local MCP server that exposes structured tools, while the Android platform serves as the central tool registry. On the MCP client side, agent apps are registered with the intelligence system after being granted system-privileged permissions to access the registry.</p>

<p>When a user interacts with a registered agent, its LLM determines if the request can be handled by an AppFunction, queries the platform's metadata, and executes the appropriate registered functions in the background. This local MCP client-server design gives you full control: you choose exactly which features are accessible to the agent, keeping the rest of your app's data private.</p>

<h2>How we accelerated development with Android skills</h2>

To streamline the integration process, we leveraged the <a href="https://github.com/android/skills/tree/main/device-ai/appfunctions">AppFunctions development skill</a>. The AppFunctions development skill is a complete development companion. It guided us through the entire lifecycle: mapping Kotlin data classes to serialize parameters, generating the necessary <code>Service</code> entry points, refining our <code>KDoc</code> documentation to ensure the LLM understands parameter boundaries, and setting up automated testing using ADB.

<h2>Providing app features to the intelligence system</h2>

<p>Enough with the theory, let's dive into the implementation.</p>

<h4>Configuration and dependency setup</h4>

<p>We begin by adding the AppFunctions dependencies. One for the API and one for the Kotlin Symbol Processing compiler.</p>

<pre><code>implementation("androidx.appfunctions:appfunctions:1.0.0-alpha10")
ksp("androidx.appfunctions:appfunctions-compiler:1.0.0-alpha10")</code></pre>

<h4>Modeling custom data types</h4>

<p>Any custom object exchanged with the agent must be annotated with <code>@AppFunctionSerializable</code>. In our <a href="https://github.com/android/ai-samples/tree/main/jetpacker/android/feature/appfunctions/src/main/java/com/example/jetpacker/feature/appfunctions/TripSerializable.kt">TripSerializable.kt</a> file, we define our trip data model:</p>

<pre><code>@AppFunctionSerializable(isDescribedByKDoc = true)
data class TripSerializable(
    /** The trip's unique identifier. */
    val id: String,
    /** The trip's title. */
    val title: String,
    /** The trip's destination location. */
    val location: String,
    /** The trip's start date in milliseconds. */
    val startDate: Long,
    /** The trip's end date in milliseconds. */
    val endDate: Long,
    /** A list of participants. */
    val participants: List&lt;String&gt;,
)</code></pre>

<h4>Providing features using the @AppFunction annotation</h4>

<p>Next, the skill wrote the Kotlin functions that perform the database queries and annotate them with <code>@AppFunction</code>. We can view this in searchTrip:</p>

<pre><code>/**
 * Looks for trips based on optional filters like id, title (name), location, and dates.
 *
 * @param id The unique identifier of the trip.
 * @param title The title or name of the trip.
 * @param location The destination location.
 * @param startDate The minimum start date in milliseconds.
 * @param endDate The maximum end date in milliseconds.
 * @return A list of trips matching the filters.
 */
@AppFunction(isDescribedByKDoc = true)
suspend fun searchTrip(
    id: String? = null,
    title: String? = null,
    location: String? = null,
    startDate: Long? = null,
    endDate: Long? = null
): List&lt;TripSerializable&gt; {
    return withContext(Dispatchers.IO) {
    // implementation
}</code></pre>

<p>Since AppFunctions run on the UI thread by default, we use <code>withContext(Dispatchers.IO)</code> to switch to a background dispatcher. Additionally, we refine our KDoc to use clear, imperative verbs and specify parameter constraints. This documentation compiles directly into the tool's schema, which the privileged agent uses to resolve parameters and handle runtime errors.</p>

<h4>The service entry point and Hilt integration</h4>

<p>To register these features with the intelligence system, we create an abstract base class that extends <code>AppFunctionService</code>. We annotate it with <code>@AppFunctionServiceEntryPoint</code>:</p>

<pre><code>@RequiresApi(36)
@AndroidEntryPoint
@AppFunctionServiceEntryPoint(
    serviceName = "JetPackerAppFunctionService",
    appFunctionXmlFileName = "jetpacker_app_function_service"
)
abstract class BaseJetPackerAppFunctionService : AppFunctionService() {
    @Inject internal lateinit var tripDao: TripDao
    // DAOs and database references are injected here...
}</code></pre>

<p>During compilation, KSP generates the final concrete service subclass, <code>JetPackerAppFunctionService</code>, as declared with the <code>serviceName</code> parameter. We also register <code>app_metadata.xml</code> in the app's manifest. This file provides global operational rules for JetPacker's declared AppFunctions.</p>

<h2>Testing and verifying your AppFunctions</h2>

<p>Once implemented, you should verify that your AppFunctions are registered and working correctly.</p>

<p>Running devices or emulators with Android 17 or newer, you can use ADB commands from your terminal to list and invoke your functions. Running <code>adb shell cmd app_function list-app-functions</code> displays all registered functions for your package. You can then execute a specific function and test its database integration by running <code>adb shell cmd app_function execute-app-function</code> while passing a raw JSON parameters string.</p>

<p>Instead of these ADB commands, you can also use the <a href="https://github.com/android/appfunctions">AppFunctions Testing Agent</a> to inspect your configuration, list and execute AppFunctions, and even see how your AppFunctions behave in a real conversational flow.</p>

<h2>Wrapping it up</h2>

<p>When thinking about app features that can be contributed to the intelligence system using AppFunctions requires a slight shift in how we think about code and documentation. AppFunctions enable you to use this new interaction model for apps, which allows using an agent to access app features..</p>

<p>First, the <a href="https://github.com/android/skills/tree/main/device-ai/appfunctions">AppFunctions development skill</a> is an essential lifecycle tool, helping you discover features, implement and refine AppFunctions for your apps. Second, KDoc comments are a compiled API asset; clear parameter descriptions directly impact the execution accuracy of the system agent. Finally, Android MCP provides local-first execution allowing apps to safely collaborate with AI agents.</p>

<p>Contributing app features through AppFunctions makes your application ready for the intelligence system. Let us know how you are adapting your apps for the agentic era!</p>

<h2>Learn more</h2>

<p>Check out the other parts of this blog post series:<br /><b><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html">Part 1:</a></b> Introduction of the app and a high-level overview.<br /><a href="http://android-developers.googleblog.com/2026/07/android-on-device-inference.html"><b>Part 2:</b></a> On-device intelligence. Deep-dive into ML Kit’s GenAI APIs and Gemini Nano to build privacy-first features like itinerary summarization, receipt parsing, and local audio processing.<br /><b><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html">Part 3:</a></b> Hybrid and cloud reasoning. Explore how to use Firebase AI Logic to ground LLM answers in real-world data like Google Maps and web context.<br /><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-appfunctions.html"><b>Part 4 (this post!):</b></a> System integration. Integrating with the Android intelligence system using AppFunctions. <br />Part 5 (coming soon):&nbsp;In-app agentic workflows. Extend the app with an end-to-end booking assistant powered by A2UI and ADK.</p>

<p>Interested in more on Android Development? Follow Android Developers on <a href="https://www.youtube.com/@AndroidDevelopers">YouTube</a> or <a href="https://www.linkedin.com/showcase/androiddev/">LinkedIn</a>!</p>

<p>
  All code snippets in this blog post follow the following copyright notice:
</p>
<pre><code>Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0</code></pre></div>

### Build intelligent Android apps: Introduction to Jetpacker (Google Play)
- **Published**: 2026-07-21T09:57:02.378-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html](https://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html)
- **Key Topics**: Google Play AI policies, AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEigBFwd7rJO49I_puODKBWFqPbpHaGyL3CTFuZBbr0HTQConFnc3JP0dL9Rr_i6wmyW0o4Ku2bvv3SEacwpC3Vc6b7cYy0aRbZKdUDudFcraYO8zcBVkrMfbrfMP9How0J1xSi91xLnR4s5Z3s-Lp6RF2SA0gU56B9nXD0NkD_CU8MT6wbgBw1tRaMWcMo/s2469/0713%20Jetpacker%20Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEigBFwd7rJO49I_puODKBWFqPbpHaGyL3CTFuZBbr0HTQConFnc3JP0dL9Rr_i6wmyW0o4Ku2bvv3SEacwpC3Vc6b7cYy0aRbZKdUDudFcraYO8zcBVkrMfbrfMP9How0J1xSi91xLnR4s5Z3s-Lp6RF2SA0gU56B9nXD0NkD_CU8MT6wbgBw1tRaMWcMo/s2469/0713%20Jetpacker%20Meta.png" style="display: none;" />
<div><i>Posted by Jolanda Verhoef, Senior Developer Relations Engineer,&nbsp;</i><i>Android Developer Relations</i></div><div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhFlbIY8mjuSzlWuS8mnGJ3v8Je-yrtFFaBHNXumMqS0rbaS32wv5HUhI4mv5pHT8ro0Rfb-duyMhK8_OeKnMyocY9s6GmC9_pgTEv6sgZoiaZpD00sODTTctYV8I4RHddKWcXAMUyTASk97cS1ysx4A2PFYB6PEeiHeN93BFgDiOTKH62ZJMig3kGP66E/s8583/0713%20Jetpacker%20Blog.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2601" data-original-width="8583" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhFlbIY8mjuSzlWuS8mnGJ3v8Je-yrtFFaBHNXumMqS0rbaS32wv5HUhI4mv5pHT8ro0Rfb-duyMhK8_OeKnMyocY9s6GmC9_pgTEv6sgZoiaZpD00sODTTctYV8I4RHddKWcXAMUyTASk97cS1ysx4A2PFYB6PEeiHeN93BFgDiOTKH62ZJMig3kGP66E/s1600/0713%20Jetpacker%20Blog.png" /></a></div><br /><i><br /></i><p>Building GenAI features in your app usually means navigating through various models, APIs and architecture choices:&nbsp;</p>
<ul>
  <li><strong>Execution location:</strong> Where does your model run? On device, in the cloud, or both?</li>
  <li><strong>Complexity:</strong> How complex is your setup? Are you doing a single inference call or do you need a more agentic flow?</li>
  <li><strong>In-app or Android System:</strong> Should your feature be built into your Android app or does it fit better as an Android system integration?</li>
</ul>

<p>In this blog post series we'll navigate these choices with you. We will take you along on a journey, starting with a basic mobile app and transforming it into a <b>personalized</b>, <b>intelligent</b>, and <b>agentic</b> experience.</p>

<h2>Jetpacker: a demo travel app</h2>
<p>Jetpacker is a <b>technical showcase app</b> that our team built from the ground up for this year's Google I/O (built using Antigravity). At its core, Jetpacker helps users plan, explore, and enjoy their next big adventure. It shows an overview of your trips, the itinerary of each trip, and details of each event on that trip. Of course following all best practices of Android development, including a beautifully expressive Material UI design.</p><div style="height: 0px; max-width: 100%; overflow: hidden; padding-bottom: 56.25%; position: relative;">
  <iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" src="https://www.youtube-nocookie.com/embed/_iuXykdlTkk" style="height: 100%; left: 0; position: absolute; top: 0; width: 100%;" title="YouTube video player">
  </iframe>
</div>

<p>And best of all? It's fully <a href="https://github.com/android/ai-samples/tree/main/jetpacker" target="_blank">open source</a>!</p>

<p>Today we are publishing a series of<b> technical blog posts</b> diving deep into each of these features. We’ll provide detailed implementation steps, code snippets, and architectural insights to help you build your own intelligent Android applications.</p>

<h2><a href="http://android-developers.googleblog.com/2026/07/android-on-device-inference.html">On-device intelligence</a></h2>
<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg7d4EqOTEFypjsqmFoZ8h-zPw3QqQkNY1F_vdbJ98vv1QJCqIE8P-reC0fttcMfNk05g3kGSLhGXVaeiOQDqARK6ptNhFe43miZgTNSmdF7V5hh6u4PhjQleWXmxDqkAf5YKPPyBU14V9z_wFfkiwVDCHN0rkLDtbZCGnb6Jq8d7Iu3YRVgDd9fcMeTiA/s1848/on-device-features.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1256" data-original-width="1848" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg7d4EqOTEFypjsqmFoZ8h-zPw3QqQkNY1F_vdbJ98vv1QJCqIE8P-reC0fttcMfNk05g3kGSLhGXVaeiOQDqARK6ptNhFe43miZgTNSmdF7V5hh6u4PhjQleWXmxDqkAf5YKPPyBU14V9z_wFfkiwVDCHN0rkLDtbZCGnb6Jq8d7Iu3YRVgDd9fcMeTiA/s1600/on-device-features.png" /></a></div><div style="text-align: center;"><i>On-device features in Jetpacker: Summarizing trip itineraries, managing expenses, and voice notes</i></div><p>Using an on-device model comes with <b>no additional cloud inference</b> costs, means you don't have to worry about <b>internet connectivity</b>, and lets users be confident that private information will be <b>processed locally</b>, on the device, without any of their data being sent to the cloud.</p>

<p>In Jetpacker, we chose on-device inference for three of our features:</p>
<ul>
  <li>The <b>trip overview</b> feature transforms a messy, multi-day itinerary into a concise, actionable summary. It leverages Gemini Nano through the <a href="https://developers.google.com/ml-kit/genai/prompt/android">ML Kit GenAI APIs</a> to process data locally on the device. We consider this a nice-to-have feature where we don't want to incur extra cloud costs, making on-device inference the right choice.</li>
  <li>The <b>expense tracker</b> automatically extracts structured data from receipt images to help users track their travel spending. It uses the <a href="https://developers.google.com/ml-kit/genai/prompt/android/get-started#provide-multimodal">multimodal capabilities</a> of Gemini Nano 4 through the ML Kit GenAI APIs. We choose an on-device solution so that any privacy-sensitive information on the receipt images never leaves the user's device.</li>
  <li>The <b>audio diary </b>records, transcribes, and categorizes voice notes into relevant trip activities. It is powered by the <a href="https://developers.google.com/ml-kit/genai/speech-recognition/android">ML Kit Speech Recognition</a> and <a href="https://developers.google.com/ml-kit/genai/prompt/android/get-started">GenAI Prompt APIs</a>. We chose an on-device solution for privacy and connectivity reasons.</li>
</ul>

<h2><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html" target="_blank">Cloud &amp; hybrid inference</a></h2>
<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiFPZiA1Obbj1gQKJ6S-U4UCR-jiUjasFY3jGQPeBRS27JJD5DzDIpGseazaNR3qcXR6xtYck8RYqKd0jgHGXVnfqQiPkW7jWVgTB_Hkds5EZcQDjosBZc7Ma9A-JaRaLeVxzEpTXYwSkalIyOIt-WQ_kqdlAvpDH1nB0Ajv7FdFJJ50aBOhP7a0p_RvN4/s2722/cloud-hybrid-features.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1632" data-original-width="2722" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiFPZiA1Obbj1gQKJ6S-U4UCR-jiUjasFY3jGQPeBRS27JJD5DzDIpGseazaNR3qcXR6xtYck8RYqKd0jgHGXVnfqQiPkW7jWVgTB_Hkds5EZcQDjosBZc7Ma9A-JaRaLeVxzEpTXYwSkalIyOIt-WQ_kqdlAvpDH1nB0Ajv7FdFJJ50aBOhP7a0p_RvN4/s1600/cloud-hybrid-features.png" /></a></div><br /><p><br /></p><p><br /></p><p><br /></p><p><br /></p><p><br /></p><p><br /></p><p><br /></p><p><br /></p><p><br /></p><p><br /></p><p><br /></p><i><div style="text-align: center;"><i>Cloud and hybrid features in Jetpacker: Museum assistant with web grounding, hybrid restaurant review drafting, and hotel support chat featuring custom-routed live translation.</i></div></i><p>Sometimes your use-case requires AI models with <b>greater world knowledge</b> or a much <b>larger context window</b> and with greater ability in <b>handling complex tasks</b>. In that case, we can switch from running an on-device model to using a cloud model instead.</p>

<p>Or, if you want to get the best of both worlds, you can use hybrid inference to <b>dynamically choose</b> either a cloud or on-device model at runtime. This allows us to <b>lower costs</b> by moving inference to the device when it is available, but at the same time <b>support all Android devices</b> running the app.</p>

<p>In Jetpacker, we implemented several features using cloud or hybrid inference:</p>
<ul>
  <li>The <b>place Q&amp;A</b> feature answers user questions about specific locations by grounding responses in real-world data. It uses <a href="https://firebase.google.com/docs/ai-logic">Firebase AI Logic</a> integrated with <a href="https://firebase.google.com/docs/ai-logic/grounding-google-maps">Google Maps</a> and <a href="https://firebase.google.com/docs/ai-logic/grounding-google-search">web context</a>. Using a cloud model is necessary here for its greater world knowledge.</li>
  <li>The <b>review drafting</b> feature helps users compose detailed reviews for the places they have visited. It leverages both on-device and cloud models through Firebase AI Logic's new <a href="https://firebase.google.com/docs/ai-logic/hybrid/android/get-started">Hybrid inference API</a>. This is a feature we wanted to make available to all app users, so we're using a cloud model as a fallback when an on-device model is unavailable.</li>
  <li>The <b>automatic chat translation</b> dynamically translates chat messages in real time to facilitate seamless communication, demonstrating custom hybrid inference logic. Again, we want this feature to be available to all app users, but at the same time have some specific considerations on when to choose on-device versus cloud.</li>
</ul>

<h2><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-appfunctions.html">System integration</a></h2><div style="height: 0px; max-width: 100%; overflow: hidden; padding-bottom: 56.25%; position: relative;">
  <iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" src="https://www.youtube-nocookie.com/embed/qtQMH8RBYIo" style="height: 100%; left: 0; position: absolute; top: 0; width: 100%;" title="YouTube video player">
  </iframe>
</div>
<p>While not a feature you see in the app itself, the Android system integration opens up the app's core capabilities directly to the Android operating system. It uses the <a href="https://developer.android.com/ai/appfunctions">AppFunctions API</a> to integrate with system-level intelligence.</p>

<h2>In-app agentic workflows (coming soon!)</h2>
<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh3YAW_TWepCinuAvHQ7i9JKfhWtf-GSggI6CtD0Qp7-nfPA7UTmmYHTAtsEybWlmiPgxZqo_fUlqc44dmF_5WWH4tlTRze8qdsm9Jc5ARwL5k_PJjU1VTcAHRE3EdxL4JHSnsCt4VCzwPaR41LM34048icLNZLE1kUhpLTeiGpDH87Bh7utPJmXS4kn_8/s1618/agentic-feature-booking-assistant%20(1).png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1618" data-original-width="844" height="400" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh3YAW_TWepCinuAvHQ7i9JKfhWtf-GSggI6CtD0Qp7-nfPA7UTmmYHTAtsEybWlmiPgxZqo_fUlqc44dmF_5WWH4tlTRze8qdsm9Jc5ARwL5k_PJjU1VTcAHRE3EdxL4JHSnsCt4VCzwPaR41LM34048icLNZLE1kUhpLTeiGpDH87Bh7utPJmXS4kn_8/w209-h400/agentic-feature-booking-assistant%20(1).png" width="209" /></a></div><i><div style="text-align: center;"><i>The booking assistant shows several in-progress flight bookings, asking the user for input before making a final booking.</i></div></i><p>Agenticness introduces a higher level of<b> autonomy</b>, enabling models to act as agents. Instead of a single inference call, an agent works towards a specific goal via an orchestration loop that allows it to <b>reason</b>, use <b>tools</b>, and <b>adapt </b>its path. Depending on your requirements, these intelligent agents can run either in the cloud, directly on-device, or in a hybrid setup.</p>

<p>For Jetpacker we added a <b>booking assistant</b> that automates end-to-end booking workflows directly within the application to streamline reservations. It is built using <a href="https://a2ui.org/">A2UI</a> and <a href="https://adk.dev/">ADK</a> running in the cloud. The Android app functions as a front-end to the multi-agentic system running in the cloud.</p>

<h2>Learn more</h2>
<p>Check out the other parts of this blog post series:</p><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html"><b>Part 1 (this post!):</b></a> Introduction of the app and a high-level overview.<br /><a href="http://android-developers.googleblog.com/2026/07/android-on-device-inference.html"><b>Part 2:</b></a> On-device intelligence. Deep-dive into ML Kit’s GenAI APIs and Gemini Nano to build privacy-first features like itinerary summarization, receipt parsing, and local audio processing.<br /><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html"><b>Part 3:</b></a> Hybrid and cloud reasoning. Explore how to use Firebase AI Logic to ground LLM answers in real-world data like Google Maps and web context.<br /><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-appfunctions.html"><b>Part 4:</b></a> System integration. Integrating with the Android intelligence system using AppFunctions.<br />Part 5 (coming soon): In-app agentic workflows. Extend the app with an end-to-end booking assistant powered by A2UI and ADK.<p>Interested in more on Android Development? Follow Android Developers on <a href="https://www.youtube.com/@AndroidDevelopers">YouTube</a> or <a href="https://www.linkedin.com/showcase/androiddev/">LinkedIn</a>!</p></div>

### Build intelligent Android apps: On-device inference (Google Play)
- **Published**: 2026-07-21T09:57:46.319-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/07/android-on-device-inference.html](https://android-developers.googleblog.com/2026/07/android-on-device-inference.html)
- **Key Topics**: AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhd7g4aJ0ZhzVcuPr3SzBJIVQ_MZT3hIXb1Ff8SVjjrvRjYzZwhgoE7IbHryS6Ds7u7if1_tmVmMdkFNAtPADXoeuRQ_64Pxfnp3oq2aHR8hbS3fDExGxE0nSiOvXPw7SonhNdjFNI2eDJfasEEMs0xjh2gZlyPq6ToimvFlaMv2-nVDz_XLnSXK1iCn4U/s2469/0625%20Building%20JetPacker%20with%20Intelligent%20On-Device%20features_Meta%20v02.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhd7g4aJ0ZhzVcuPr3SzBJIVQ_MZT3hIXb1Ff8SVjjrvRjYzZwhgoE7IbHryS6Ds7u7if1_tmVmMdkFNAtPADXoeuRQ_64Pxfnp3oq2aHR8hbS3fDExGxE0nSiOvXPw7SonhNdjFNI2eDJfasEEMs0xjh2gZlyPq6ToimvFlaMv2-nVDz_XLnSXK1iCn4U/s2469/0625%20Building%20JetPacker%20with%20Intelligent%20On-Device%20features_Meta%20v02.png" style="display: none;" /><div><i>Posted by Caren Chang, Developer Relations Engineer, Android Developer Relations</i></div><div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgIU-6haqWEXnugbhG5is8t1TU0tN3EkfSc7GwvHMRsMSU14k-P7q4il_nJlGk-qNP_PG3aKs1LDWNgWKqhFsG6Q16v2zeoHMvqY_PesC5ddxHRjTGgtiQ33uvOrUIPkSdUgFfBIYSkqBhcuZJTY8jbW0mOjKs8XF8DLxfyD7CjJ1Sd4FM7AUrufTnSEVw/s8582/0625%20Building%20JetPacker%20with%20Intelligent%20On-Device%20features_Blog%20v02.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2601" data-original-width="8582" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgIU-6haqWEXnugbhG5is8t1TU0tN3EkfSc7GwvHMRsMSU14k-P7q4il_nJlGk-qNP_PG3aKs1LDWNgWKqhFsG6Q16v2zeoHMvqY_PesC5ddxHRjTGgtiQ33uvOrUIPkSdUgFfBIYSkqBhcuZJTY8jbW0mOjKs8XF8DLxfyD7CjJ1Sd4FM7AUrufTnSEVw/s1600/0625%20Building%20JetPacker%20with%20Intelligent%20On-Device%20features_Blog%20v02.png" /></a></div><br /><i><br /></i><div><i><br /></i><p>Welcome back to the blog post series "<a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html" target="_blank">Build intelligent Android apps</a>" where we take a basic Android app and transform it into a <b>personalized, intelligent, </b>and <b>agentic </b>experience. In our <a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html" target="_blank">previous post we introduced Jetpacker</a>, the demo app we'll use throughout this series.</p>

<p>In this blog post, we will share how you can use Gemini Nano through <a href="https://developers.google.com/ml-kit/genai/prompt/android">ML Kit’s Prompt API</a> to build intelligent on-device features.</p>
<div style="height: 0px; margin: 0px auto; max-width: 853px; overflow: hidden; padding-bottom: 56.25%; position: relative;">
  <iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" src="https://www.youtube-nocookie.com/embed/_iuXykdlTkk" style="height: 100%; left: 0; position: absolute; top: 0; width: 100%;" title="YouTube video player">
  </iframe>
</div>

<p>Building intelligent on-device features refers to the ability to process prompts and data directly on a device without sending data to a server. This offers a few advantages:</p>
<ul>
  <li>User data can be processed <b>locally</b> on the device, preserving user privacy</li>
  <li>Functionality of the model is <b>reliable</b> even with spotty or no internet connection</li>
  <li>No additional cloud inference <b>cost</b>, since everything runs on the user’s hardware</li>
</ul>

<p>With the benefits of on-device in mind, we identified three features to add in Jetpacker that can improve the user experience: summarizing trip itineraries, managing expenses, and capturing voice notes.</p>

<h2><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg3FDrGSpGJqSapXXQ7052s1NR8rzvmmW-xbyOaAcg8bdTA6ZH7p6ZWE664FjlaoDLfREd-RlQil7gV-VjnCoq76o06haLoSxBzlIDAvM-dKvm_TCgPvqHU3ZlzBTXZ9XtAyMk26QWB8PvU5aUmzO0RBuMxqxJdC1wk7xl_1PXd1KHvuMCeHeAP9zhgSjg/s1848/Screenshot%202026-07-02%20at%2012.57.08%E2%80%AFPM.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1256" data-original-width="1848" height="434" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg3FDrGSpGJqSapXXQ7052s1NR8rzvmmW-xbyOaAcg8bdTA6ZH7p6ZWE664FjlaoDLfREd-RlQil7gV-VjnCoq76o06haLoSxBzlIDAvM-dKvm_TCgPvqHU3ZlzBTXZ9XtAyMk26QWB8PvU5aUmzO0RBuMxqxJdC1wk7xl_1PXd1KHvuMCeHeAP9zhgSjg/w640-h434/Screenshot%202026-07-02%20at%2012.57.08%E2%80%AFPM.png" width="640" /></a></div><div style="text-align: center;"><span style="font-weight: normal;"><span style="font-size: small;"><i>On-device features in Jetpacker: Summarizing trip itineraries, managing expenses, and voice notes</i></span></span></div><div class="separator" style="clear: both; text-align: center;"><br /></div>High quality tailored summarization of short texts</h2>

<p>The itinerary screen gives users a quick overview of all activities for a given trip. Since this screen contains a lot of information, it can quickly become overwhelming. To help users prepare without feeling overwhelmed, we can add a ‘<b>Get ready for your trip</b>’ section at the top.</p>
<p style="text-align: center;"><em></em></p>
<div class="separator" style="clear: both; text-align: center;"><em><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtWrJplvxl7ymB4kMN_Tg4tYYkL7G1Ory0hSptzqsbw_xCu4I9l_4SQPQ9CUXs_Jc7qtT1KcpltBds0aYgIvXiK_-qp6fnoX3QmYnGyqGgr2d5f2uzQkyMK-_Iebwp9Ap0aJA4c8Pz4Zy01O5AM6kk_qZ4Blx_bY-_2xIxSA8DMva2LWBbCN_Hb_c37KE/s2499/Screenshot_20260702_111934.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="2499" data-original-width="1183" height="400" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtWrJplvxl7ymB4kMN_Tg4tYYkL7G1Ory0hSptzqsbw_xCu4I9l_4SQPQ9CUXs_Jc7qtT1KcpltBds0aYgIvXiK_-qp6fnoX3QmYnGyqGgr2d5f2uzQkyMK-_Iebwp9Ap0aJA4c8Pz4Zy01O5AM6kk_qZ4Blx_bY-_2xIxSA8DMva2LWBbCN_Hb_c37KE/w189-h400/Screenshot_20260702_111934.png" width="189" /></a></em></div>
<div style="text-align: center;"><span style="font-weight: normal;"><span style="font-size: small;"><i>The romantic Paris trip is summarized as a classic Parisian adventure blending art, sights, and delicious food. A tip and some useful phrases are also added.</i></span></span></div>
<p></p>

<p>By inputting a trip itinerary and asking an LLM to summarize it, we can generate a quick summary of the trip along with packing tips and useful local phrases. This is a great use case for an on-device model for several reasons:</p>
<ul>
  <li><b>Performance and quality</b>: Both the input and output text are relatively short. With that, we can expect the performance and quality of an on-device solution to be on par with more powerful cloud models.</li>
  <li><b>Scalability</b>: Shifting inference on-device allows us to scale this feature from a few users to millions without worrying about managing increasing cloud inference costs.</li>
  <li><b>Low latency and reliability</b>: On-device inference guarantees low latency, providing a reliable experience even when users are offline.</li>
</ul>

<p>To build with on-device, we use <b>Gemini Nano</b>, Google’s most efficient model optimized for mobile devices. Gemini Nano was first introduced a few years ago, and is now running on over 140 million devices. The latest version of the model, <a href="https://android-developers.googleblog.com/2026/04/AI-Core-Developer-Preview.html">Gemini Nano 4, is built on the architecture foundation of the recently released Gemma 4 model</a>, and is further optimized for maximum battery and performance efficiency.</p>

<p>Using ML Kit’s <b>Prompt API</b>, we can take advantage of Gemini Nano 4’s new model capabilities to prototype our on-device features. We’ll create a prompt that includes the itinerary of a trip and ask the model to generate a summary along with any preparation tips.</p>

<pre><code>// implementation("com.google.mlkit:genai-prompt:1.0.0-beta3")

// Define the configuration for Gemini Nano 4 E2B preview model
val previewFastConfig = generationConfig {
    modelConfig = modelConfig {
        releaseStage = ModelReleaseStage.PREVIEW
        preference = ModelPreference.FAST
    }
}

val geminiNano2BPreviewModel = Generation.getClient(previewFastConfig)

val tripItinerary = ...

val getReadyForYourTripSummary = geminiNano2BPreviewModel
 .generateContent("Given this trip itinerary: $tripItinerary,
     generate the following: overall vibe, tips on how to prepare for this
     trip, and common short phrases to learn for the trip.")</code></pre>

<p>Finding the optimal prompt usually requires some iteration, and the AICore app is perfect for this step in the process. After opting into the <a href="https://developers.google.com/ml-kit/genai/aicore-dev-preview">developer preview option for AICore</a>, we can download preview models such as Gemini Nano 4 to test prompts and see the model’s expected outputs. With a few iterations on the prompt, we were able to improve the speed of the response from 13 seconds to under 2 seconds! Check out the final code implementation and prompt <a href="https://github.com/android/ai-samples/blob/40b999ef0e85693eac4de06e58335f0f5f125fa6/jetpacker/android/feature/trip/itinerary/enrichment/src/main/kotlin/com/example/jetpacker/feature/itinerary_enrichment/TripSummaryAndTipsProviderImpl.kt#L100" target="_blank">here</a>.</p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiaY2Q7rzlrAj2i410lc3qqtKwI3m6ufAi27R5S94LVFJKEJPnxmvShIcAWdD_Cx9lhTz9tmKW_DVcmNg0rZFBKpqYj0M9niFJwa-AurlyV2SHuErI7Z9H59Q9S936I4ErUQ_NFRNSJpUBXwDVmw6vKNVpIkBrYPJNUpCIyNXl5Z17x7jEl5Kn9BGgFuLg/s553/Screen%20Recording%202026-07-02%20at%2012.28.51%E2%80%AFPM.gif" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="553" data-original-width="496" height="400" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiaY2Q7rzlrAj2i410lc3qqtKwI3m6ufAi27R5S94LVFJKEJPnxmvShIcAWdD_Cx9lhTz9tmKW_DVcmNg0rZFBKpqYj0M9niFJwa-AurlyV2SHuErI7Z9H59Q9S936I4ErUQ_NFRNSJpUBXwDVmw6vKNVpIkBrYPJNUpCIyNXl5Z17x7jEl5Kn9BGgFuLg/w359-h400/Screen%20Recording%202026-07-02%20at%2012.28.51%E2%80%AFPM.gif" width="359" /></a></div>

<div style="text-align: center;"><span style="font-weight: normal;"><span style="font-size: small;"><i>The first iteration of our prompt generated way too many tokens, and optimizing it helped keep responses quick and to the point.</i></span></span></div>

<h2>Local processing for sensitive user input</h2>

<p>Next, to help users enjoy their trip even more, we’ll build a simple expense manager that takes the manual work out of sorting through receipts and calculating budgets.</p>
<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgsHCjYJhDefKk1_FHnyB8mXO6XGrVWPrWkkxUikHNrWly2YqLjD8GyN-qGXOBlZCJPug-VbVgBr8awg8I-TEl6d9udKhq_zKem9Xcdb7FzFlA4B77Iko2Rbf8R0XIPB30owcMoh-7KJ1paQnzDrNHSdvwYotNxt166QqJdNAf1d8wEwIFkL9qIEYUKmoQ/s1282/7.13_BlogGif_Transparent.gif" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1282" data-original-width="613" height="400" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgsHCjYJhDefKk1_FHnyB8mXO6XGrVWPrWkkxUikHNrWly2YqLjD8GyN-qGXOBlZCJPug-VbVgBr8awg8I-TEl6d9udKhq_zKem9Xcdb7FzFlA4B77Iko2Rbf8R0XIPB30owcMoh-7KJ1paQnzDrNHSdvwYotNxt166QqJdNAf1d8wEwIFkL9qIEYUKmoQ/w191-h400/7.13_BlogGif_Transparent.gif" width="191" /></a></div>
<br />

<div style="text-align: center;"><span style="font-weight: normal;"><span style="font-size: small;"><i>Taking a photo of a restaurant bill, data is parsed and shown in the expense overview screen of the app.</i></span></span></div>

<p>Since receipts might contain sensitive information like credit card number and addresses, this is another great use case for an on-device solution. With on-device, users can be confident that private information will be processed locally on the device without any of their data being sent to the cloud.</p>

<p>In addition, Gemini Nano 4 has improved model capabilities for multimodality, especially for image understanding tasks like OCR and visual data extraction, making it a great solution for tasks like extracting information from receipts.</p>

<p>For this use case, the prompt will analyze an image of the receipt, and output information such as: a generated title, amount spent and category of the expense. To ensure the model outputs the information in the preferred format, we can use <a href="https://developers.google.com/ml-kit/genai/prompt/android/structured-output">ML Kit’s Structured Output API</a> to seamlessly output a Kotlin data object that we define.</p>

<pre><code>// implementation("com.google.mlkit:genai-prompt:1.0.0-beta3")
// ksp("com.google.mlkit:genai-schema-compiler:1.0.0-alpha1")

@Generable("Information extracted from an expense receipt")
data class ParsedReceipt(
  @Guide("Generated title for the expense less than 6 words. Based on restaurant or activity name.")
  val title: String,
  @Guide("Total amount of the expense. Look for values at the bottom and words like total or balance due.")
  val amount: Double,
  @Guide("Type of expense", enumValues = ["travel", "food", "shopping", "entertainment", "other"])
  val category: String,
)

val prompt = "Determine if the image is a receipt or expense.
    If it is NOT a receipt or expense, output the text 'NOT_A_RECEIPT'.
    Otherwise, parse the receipt information."

val request = generateContentRequest(ImagePart(bitmap), TextPart(prompt)) {}
val requestWithStructuredOutput = generateTypedContentRequest(request, ParsedReceipt::class)

// Define the configuration for Gemini Nano 4 E4B preview model
// When selecting models, you can specify which performance charactertists are most important
//  for your use case. Use ModelPreference.FULL when you want to prioritize reasoning power over speed.
//  Use ModelPreference.FAST when complex logic is not required and latency is a priority.
val previewFullConfig = generationConfig {
    modelConfig = modelConfig {
        releaseStage = ModelReleaseStage.PREVIEW
        preference = ModelPreference.FULL
    }
}

val geminiNano4BPreviewModel = Generation.getClient(previewFullConfig)
val response = geminiNano4BPreviewModel.generateContent(requestWithStructuredOutput)
val parsedReceipt: ParsedReceipt? = response.candidates.firstOrNull()?.response</code></pre>

<h2>Multimodal input</h2>

<p>Lastly, to help users record audio memos during the trip, let’s build a fully on-device voice notes feature. Using <a href="https://developers.google.com/ml-kit/genai/speech-recognition/android">ML Kit’s Speech Recognition API</a>, we’ll enable users to record short voice notes that are automatically transcribed to text. With the transcribed text, we’ll use ML Kit’s Prompt API to identify which trip activity is associated with the recorded voice note, letting users easily recap their trip as they scroll through the trip’s itinerary.</p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjnAm4XPVEJkfPmRFKJWh2sS-4rVz_eFollYxU5DWb7kAkSQdP4xhAEosziS_vpxv6yoAkvHiSp6SGYOp2_qp_cJWgfbJGnDOadaMP6Bc30a6rYnSP34sEubNAWXqsmd3cpYOoL8rCUhQn0_4GT3165aSFinlnHZjVnXYNYBAw8AdVtJpuRG2gDbi-uRII/s2499/Screenshot_20260702_115529.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="2499" data-original-width="1183" height="400" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjnAm4XPVEJkfPmRFKJWh2sS-4rVz_eFollYxU5DWb7kAkSQdP4xhAEosziS_vpxv6yoAkvHiSp6SGYOp2_qp_cJWgfbJGnDOadaMP6Bc30a6rYnSP34sEubNAWXqsmd3cpYOoL8rCUhQn0_4GT3165aSFinlnHZjVnXYNYBAw8AdVtJpuRG2gDbi-uRII/w189-h400/Screenshot_20260702_115529.png" width="189" /></a></div>

<p style="text-align: center;"><em>The Roman holiday itinerary shows voice note extracts.</em></p>

<p>The <a href="https://developers.google.com/ml-kit/genai/speech-recognition/android">ML Kit GenAI Speech Recognition API </a>allows you to transcribe audio content to text fully on-device using two distinct modes. <b>Basic mode</b> uses a traditional on-device speech recognition model and is available on most Android devices with API level 31 and higher. <b>Advanced mode</b> uses Gemini Nano to offer broader language coverage and better quality, and is currently supported on Pixel 10 devices.</p>

<p>For our feature we combine the Speech Recognition API with the ML Kit GenAI Prompt API:</p>

<pre><code>// implementation("com.google.mlkit:genai-prompt:1.0.0-beta3")
// implementation("com.google.mlkit:genai-speech-recognition:1.0.0-alpha1")

val tripEvents = ...

// Set up speech recognition
val speechRecognizerOptions =
    speechRecognizerOptions {
        locale = Locale.US
        preferredMode = SpeechRecognizerOptions.Mode.MODE_ADVANCED
    }
val speechRecognizer: SpeechRecognizer = SpeechRecognition.getClient(speechRecognizerOptions)

suspend fun transcribeVoiceNote(recognizer: SpeechRecognizer) {
    // Display partial text as the user is recording audio
    var partialTextResponse = ""

    // Display the full text once user is finished recording audio
    var transcription = ""

    val request: SpeechRecognizerRequest
        = speechRecognizerRequest { audioSource = AudioSource.fromMic() }
    recognizer.startRecognition(request).collect { response -&gt;
        when (response) {
            is SpeechRecognizerResponse.PartialTextResponse -&gt; {
                partialTextResponse = response.text
            }
            is SpeechRecognizerResponse.FinalTextResponse -&gt; {
                transcription = response.text
                processAndCategorizeVoiceNote(transcription, tripEvents)
            }
        }
    }
}

fun processAndCategorizeVoiceNote(transcribedVoiceNote: String, events: List<event>) {
    val prompt = "Given the voice note $transcribedVoiceNote
     and the following events for this trip: $events, rewrite this transcription
     to remove filler words. Then, identify which events from the
     list this rewritten transcription matches to."

     // Utilize ML Kit's Prompt API to process voice note and tag it with the relevant trip activities
     Generation.getClient().generateContent(prompt)
}</event></code></pre>

<h2>Conclusion</h2>

<p>Using ML Kit’s GenAI APIs, we were able to take advantage of Gemini Nano to develop fully on-device intelligent features for the JetPacker app, and provide an improved user experience without any additional cloud costs.</p>

<p>Check out the full source code for <a href="https://github.com/android/ai-samples/tree/main/jetpacker" target="_blank">Jetpacker on Github</a>, and watch the video <a href="https://www.youtube.com/watch?v=_iuXykdlTkk">Build Intelligent Android apps with Google’s AI</a> to learn more about how to integrate intelligent features directly into your app using on-device models, cloud-powered reasoning, and the latest agentic frameworks.</p><h2>Learn more</h2>

<p>Check out the other parts of this blog post series:</p><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-introduction-jetpack.html"><b>Part 1:</b></a> Introduction of the app and a high-level overview.<br /><a href="http://android-developers.googleblog.com/2026/07/android-on-device-inference.html"><b>Part 2 (this post!):</b></a>&nbsp;On-device intelligence. Deep-dive into ML Kit’s GenAI APIs and Gemini Nano to build privacy-first features like itinerary summarization, receipt parsing, and local audio processing.<br /><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-cloud-hybrid-inference.html"><b>Part 3:</b> </a>Hybrid and cloud reasoning. Explore how to use Firebase AI Logic to ground LLM answers in real-world data like Google Maps and web context.<br /><a href="http://android-developers.googleblog.com/2026/07/build-intelligent-android-apps-appfunctions.html"><b>Part 4:</b></a> System integration. Integrating with the Android intelligence system using AppFunctions.<br />Part 5 (coming soon): In-app agentic workflows. Extend the app with an end-to-end booking assistant powered by A2UI and ADK.

<p>Interested in more on Android Development? Follow Android Developers on <a href="https://www.youtube.com/@AndroidDevelopers">YouTube</a> or <a href="https://www.linkedin.com/showcase/androiddev/">LinkedIn</a>!</p>

<p>All code snippets in this blog post follow the following copyright notice:<br />
</p><pre><code>Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0</code></pre><p></p></div></div>

### Upcoming Changes to the Nearby Connections API (Google Play)
- **Published**: 2026-07-20T09:00:55.199-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/07/upcoming-changes-nearby-connections-api.html](https://android-developers.googleblog.com/2026/07/upcoming-changes-nearby-connections-api.html)
- **Key Topics**: AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhBTEW5VPkXYGqZfx-TbWnVWxTk9AQIL8sALc8flpOeFh0cKmglsMQvlLpFfLk1Hk5dGxbj96UE_vLtNjxH91AIS583psy8RmP91l0TYuP2hXJPt5c-IZGmmU66d9FNlu9T-s9myFA9_uoQ60n-uy1DK96flaQSUkjh1nN2z3jMKOL4qMPg14XOlpH122Y/s2469/Upcoming%20Changes%20to%20the%20Nearby%20Connections%20API%20_Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta><i>Posted by Wei Wang, Engineering Manager, Android BeTo</i>

<div class="separator" style="clear: both; text-align: justify;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjG84rk4vo20t7pFUGFUp6Cx38qbJTZWW5Q5ztSfPOaV474gZ4mnT7qpnC6o4hKJkwR6CiD4TwPWCS0aU-w0nr70WkKrcpR2yRM5PXnMDa9t3mjgQVahNBzLijD2v23LiDj_NaMWoyVXWTV3cKXHsForureZTA1_Q5M_03ZAve7PybnhpYpGG05IS2uCv0/s8583/Upcoming%20Changes%20to%20the%20Nearby%20Connections%20API%20_Blog.png" style="clear: left; float: left; margin-bottom: 0.3em; margin-right: 1em;"><img border="0" data-original-height="2600" data-original-width="8583" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjG84rk4vo20t7pFUGFUp6Cx38qbJTZWW5Q5ztSfPOaV474gZ4mnT7qpnC6o4hKJkwR6CiD4TwPWCS0aU-w0nr70WkKrcpR2yRM5PXnMDa9t3mjgQVahNBzLijD2v23LiDj_NaMWoyVXWTV3cKXHsForureZTA1_Q5M_03ZAve7PybnhpYpGG05IS2uCv0/s1600/Upcoming%20Changes%20to%20the%20Nearby%20Connections%20API%20_Blog.png" /></a></div>

<p style="margin-bottom: 0.3em; margin-top: 0.3em;">User privacy and transparency are core to the Android experience. To better align with these principles, we are updating the default behavior of the Nearby Connections API regarding how it interacts with device radios.</p>

<h2 style="margin-bottom: 0.5em; margin-top: 1.5em;">What is changing?</h2>
<p style="margin-bottom: 0.3em; margin-top: 0.1em;">Previously, the Nearby Connections API could automatically toggle Wi-Fi and Bluetooth radios ON to facilitate connections without explicit user intervention. Moving forward, the API will no longer automatically enable these radios for 1P and 3P applications.</p>

<h2 style="margin-bottom: 0.5em; margin-top: 1.5em;">What this means for developers</h2>
<p style="margin-bottom: 0.3em; margin-top: 0.1em;">If your app relies on Nearby Connections, you will need to update your implementation to account for these changes:</p>
<ul style="margin-bottom: 0.3em; margin-top: 0.1em;">
  <li style="margin-bottom: 0.2em;"><strong>Manual Radio Management:</strong> You must ensure that the necessary radios (Wi-Fi or Bluetooth) are enabled before initiating Nearby Connections tasks.</li>
  <li style="margin-bottom: 0.2em;"><strong>User Notification:</strong> If the required radios are disabled, your app must now inform the user and request that they enable them manually. The API will no longer programmatically turn them on for you.</li>
</ul>

<h2 style="margin-bottom: 0.5em; margin-top: 1.5em;">Timing</h2>
<p style="margin-bottom: 0em; margin-top: 0.1em;">These changes are scheduled to take effect in late 2026. We recommend reviewing your connection workflows now to ensure a seamless transition for your users.</p>

### Android Studio Quail 2 is Stable: Multi-task with the Android Studio AI agent (Google Play)
- **Published**: 2026-07-14T06:44:50.199-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/android-studio-quail-2-stable-features.html](https://android-developers.googleblog.com/2026/06/android-studio-quail-2-stable-features.html)
- **Key Topics**: General Google Play AI policy
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEitwUFdkGaqVNsaJ2iCtprD4WZuFjvI1rR6WX35ewxin0wbtVadUtkRb3qYG-KGEKepmtC4WFv2mSAmUBRmZ-oR5ey_-codg1_MhbagflhqgWk2MdNX6-yL8SaADve6mn3v0aJ_uh-qLizIgdImHaQ_KdJfVYqvCga_v_fyJYPHKDyhuhVklAfo145xays/s2461/QuailBlog_Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEitwUFdkGaqVNsaJ2iCtprD4WZuFjvI1rR6WX35ewxin0wbtVadUtkRb3qYG-KGEKepmtC4WFv2mSAmUBRmZ-oR5ey_-codg1_MhbagflhqgWk2MdNX6-yL8SaADve6mn3v0aJ_uh-qLizIgdImHaQ_KdJfVYqvCga_v_fyJYPHKDyhuhVklAfo145xays/s2461/QuailBlog_Meta.png" style="display: none;" /><p>Posted by Amman Asfaw, Product Manager, Android Studio</p><p></p><p></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh-nTZM4cgutSVcLIdjSDqJoeiaES_FELwFC84O01Roy0P81-mAyqz3X2w4pwzAZwdhiMeUuhRSyT4euWZkWtGderw6LRu-fK6k-w8lB-9k7GMXOFBy0IzgtGmUk6QkRriFX24lchlTD0SQhbywxli4p4iZ7JzMAN80YoCdruEeruJ58bwhmuo0cj9Y_yg/s2152/QuailMovement_V1_a.gif" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="608" data-original-width="2152" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh-nTZM4cgutSVcLIdjSDqJoeiaES_FELwFC84O01Roy0P81-mAyqz3X2w4pwzAZwdhiMeUuhRSyT4euWZkWtGderw6LRu-fK6k-w8lB-9k7GMXOFBy0IzgtGmUk6QkRriFX24lchlTD0SQhbywxli4p4iZ7JzMAN80YoCdruEeruJ58bwhmuo0cj9Y_yg/s1600/QuailMovement_V1_a.gif" /></a></div><br /><p></p><p><br /></p><p><br /></p><p><br /></p>

<p>Android Studio Quail 2 is now stable and ready for you to use in production, bringing a shift to your IDE with concurrent agentic workflows, natively integrated memory leak profiling, and context-aware crash remediation. Whether you are performing a sweeping architectural overhaul, tracing a memory leak, or resolving a critical production crash, Android Studio keeps you anchored in your workspace by reducing manual friction.</p>
<p style="margin-bottom: 12px;">Here’s a deep dive into what’s new:</p>
<h2 style="margin-top: 0px;">Multi-tasking with parallel chats</h2>

<p>In Android Studio Quail 2, we've been hard at work redesigning Agent Mode from the ground up. This new architecture provides better performance, offers more flexibility for decomposing complex tasks, and improves the suite of internal tools the agent uses to do its work.</p>In addition to these behind-the-scenes improvements, these changes also allow you to converse across multiple agent chats simultaneously. Waiting for the Android Studio agent to finish a task before you can ask another question or initiate a separate task in Agent Mode is a bottleneck of the past. You can multi-task seamlessly: kick off a UI refactor in one tab, fix a ProGuard rule in a second, and generate documentation in a third.<br /><br /> You can also change which models the agent uses from chat to chat based on the requests you have. Take a look at <a href="http://d.android.com/bench">Android Bench</a> for an analysis of how LLMs perform Android development tasks.

<p></p><ul style="text-align: left;"><li><strong>How to use:</strong> Click the "+" icon to start a new parallel conversation, and use the <b>History</b> icon to navigate between active tasks. Alternatively, select File &gt; New &gt; New Agent Tab to open a conversation in a dedicated tab.</li><li><strong>Note:</strong> Worktree support is currently unavailable. Exercise caution when running concurrent chats that modify the same project files, which can potentially lead to editor conflicts.</li></ul><p></p>

<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/U6T67Lbar-w" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="U6T67Lbar-w"></iframe>
</div>

<p style="text-align: center;"><i>Run multiple agent tasks in parallel with different models of your choice.</i></p><p style="text-align: center;"></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgwUDucsd939pAvvfRC8VvmNkDp-1nDBMaP3TGFwdjspFgPz7_CVS-7NVzNhP278oKO3MNJL0RZy3k9aCZgmVtuqsahIZh79bGXhB026yKqPPiMYVMFkkSUgTBSLLajNObkMkke_iF6i_cIMRRQ_5Zl8zLgXWKYItToSiyLaZfok-pd-KVkAkRfup_yCsI/s3456/Screenshot%202026-06-17%20at%2012.56.57%E2%80%AFAM.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2044" data-original-width="3456" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgwUDucsd939pAvvfRC8VvmNkDp-1nDBMaP3TGFwdjspFgPz7_CVS-7NVzNhP278oKO3MNJL0RZy3k9aCZgmVtuqsahIZh79bGXhB026yKqPPiMYVMFkkSUgTBSLLajNObkMkke_iF6i_cIMRRQ_5Zl8zLgXWKYItToSiyLaZfok-pd-KVkAkRfup_yCsI/s1600/Screenshot%202026-06-17%20at%2012.56.57%E2%80%AFAM.png" /></a></div><span style="text-align: left;"><div style="text-align: center;"><i>Use the History icon to navigate between active tasks.</i></div></span><p></p>

<h2 style="margin-top: 12px;">Memory leak detection with LeakCanary</h2>

<p>Memory leaks in Android occur when your code holds onto an object's reference long after its life cycle has ended. This prevents the Garbage Collector from reclaiming that memory, eventually leading to sluggish performance or <code>OutOfMemoryError</code>.</p>

<p>Hunting down memory leaks can be a tedious, manual task. Starting with Android Studio Quail 2, the popular open-source leak detector <a href="https://square.github.io/leakcanary/">LeakCanary</a> is natively integrated directly into the Profiler as a dedicated, first-class task.</p>

<p>This integration transforms your debugging performance by lifting and shifting the heap analysis off your resource-constrained testing phone, and onto your powerful development computer. By running the analysis on your computer, leak tracing is up to five times faster and jank-free, leaving your test app running smoothly on the device.</p>

<p>Once a leak is detected during a profiling session:</p>
<ul>
  <li>The Profiler renders an interactive, color-coded leak trace, grouping occurrences and estimating lost memory.</li>
  <li>You can click <b>Go to declaration</b> on any leaking object in the trace to instantly jump to that exact line of code in your editor.</li>
  <li>You can click <b>Fix with Agent</b> to have the Gemini agent ingest the trace, explain the root cause of the retained reference, and write the exact code change (such as unbinding a listener or clearing a static reference) to plug the leak.</li>
</ul>

<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjwBONeahZYC_5KBtkgQkc5vTjzmN5D-ypyOOScCRcp6Cy8CZeNHVWeNViBS6D_we7HaRy_AjIg1tptZAVEqNTeQ4IVVjoQp4_XJp45648fhiD0H5qvNmiPphikYGDNbEyus-QTVkSU9imwJm4QN0CKnWFs6JZsVkC21SXl9LXAnSndereOvE6iDWOmsEo/s1250/Leak_Canary_4e3675ccb2_ZXI2sE.webp" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="640" data-original-width="1250" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjwBONeahZYC_5KBtkgQkc5vTjzmN5D-ypyOOScCRcp6Cy8CZeNHVWeNViBS6D_we7HaRy_AjIg1tptZAVEqNTeQ4IVVjoQp4_XJp45648fhiD0H5qvNmiPphikYGDNbEyus-QTVkSU9imwJm4QN0CKnWFs6JZsVkC21SXl9LXAnSndereOvE6iDWOmsEo/s1600/Leak_Canary_4e3675ccb2_ZXI2sE.webp" /></a><span style="text-align: left;"><i>Review memory leaks identified via LeakCanary through the Fix with Agent button.</i></span></div>

<h2 style="margin-top: 12px;">App Quality Insights agent integration</h2>

<p>Tracking down the root cause of an app crash can require manually synthesizing stack traces, device data, and source code. However Android Studio’s App Quality Insights (AQI) is now fully integrated with Agent Mode to do the heavy lifting for you.</p>

<p>When you click on a crash in the AQI panel, you immediately get a concise, high-level summary of the issue. If you need to dig deeper, simply click <b>See more</b>. This opens a dedicated chat where the agent uses your selected model and pulls in local source code and the full stack trace to deliver a comprehensive explanation of the failure.</p>

<p>With the new agent integration, you move directly from issue identification to resolution. By clicking <b>Fix with AI</b>, the agent will analyze the issue, propose a step-by-step fix plan, and—upon your approval—apply the necessary code changes directly to your project and verify the resulting fix</p>

<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/JjgEePciHHg" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="JjgEePciHHg"></iframe>
</div><p style="text-align: center;"><i>The <b>Fix with AI</b> button triggering the agent to analyze the issue, then propose the fix</i></p>

<h2 style="margin-top: 12px;">Quality &amp; stability improvements</h2>

<p>Beyond new features, we’ve continued our focus on quality by addressing numerous bugs and incorporating the latest stability and performance improvements from the IntelliJ platform, making this a significant enhancement for your daily development.</p>

<h2 style="margin-top: 12px;">Get Started</h2>

<p>Ready to dive in and accelerate your development? <a href="https://developer.android.com/studio">Download</a> Android Studio Quail 2 and start exploring these new features today! As always, your feedback is crucial to us. <a href="https://developer.android.com/studio/known-issues">Check known issues</a>, <a href="https://developer.android.com/studio/report-bugs">report bugs</a>, and be part of our vibrant community on <a href="https://www.linkedin.com/showcase/androiddev/posts/?feedView=all">LinkedIn</a>, <a href="https://medium.com/androiddevelopers">Medium</a>, <a href="https://www.youtube.com/c/AndroidDevelopers/videos">YouTube</a>, or <a href="https://twitter.com/androidstudio">X</a>.&nbsp;</p>

### Evolving how LLMs are measured for Android: the next era of Android Bench (Google Play)
- **Published**: 2026-07-08T08:59:12.713-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/07/android-bench-llm-measurement.html](https://android-developers.googleblog.com/2026/07/android-bench-llm-measurement.html)
- **Key Topics**: General Google Play AI policy
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgCAy4lIbOAOrygTMaHZB8q4NarDrLRsqALfsmer5urQX7G_MaRDTw51uMh77Ks2knIuWM-zaEel63Dk2IlCVGD9IxLFy0B68KxwxsvDZzVDaEWaM4Bg8xJYinunaXS_fonxBw7-R4_qSplI4MJU7RDDaYlbq7nRXZoht5lFZVC7ErLEWHdWA6B2KgJvrk/s2469/Bench%20July%20releas%20V01_Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgCAy4lIbOAOrygTMaHZB8q4NarDrLRsqALfsmer5urQX7G_MaRDTw51uMh77Ks2knIuWM-zaEel63Dk2IlCVGD9IxLFy0B68KxwxsvDZzVDaEWaM4Bg8xJYinunaXS_fonxBw7-R4_qSplI4MJU7RDDaYlbq7nRXZoht5lFZVC7ErLEWHdWA6B2KgJvrk/s2469/Bench%20July%20releas%20V01_Meta.png" style="display: none;" />
<div><i>Posted by Zoe Lopez-Latorre, Senior Developer Relations Engineer, Android</i></div><div><i><br /></i><div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi49z_u9zPMjp-zyQ1yIpzLgDumtzUwZoprtIgPXv_kpF05e87KklDEguaKSJVhvV8dZJ7aVr98p-MG3FR4Sk37rcYTS91J3ADUQot-c-xnOuyIZ411VO4Hp43Yp7V_TwF6zO6RmAJpw51ZHPGbHfOwZxWgQ62SQeXblULcSc0RjMcZbLHGUZGgHzU6pEo/s8583/Bench%20July%20releas%20V01_Blog.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2601" data-original-width="8583" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi49z_u9zPMjp-zyQ1yIpzLgDumtzUwZoprtIgPXv_kpF05e87KklDEguaKSJVhvV8dZJ7aVr98p-MG3FR4Sk37rcYTS91J3ADUQot-c-xnOuyIZ411VO4Hp43Yp7V_TwF6zO6RmAJpw51ZHPGbHfOwZxWgQ62SQeXblULcSc0RjMcZbLHGUZGgHzU6pEo/s1600/Bench%20July%20releas%20V01_Blog.png" /></a></div><br /><i><br /></i><p>Back in March, we introduced <a href="http://d.android.com/bench">Android Bench</a>—our LLM leaderboard for real-world Android development tasks. Our goal was to provide transparency around model capabilities in Android development and to encourage model improvements, to give you more helpful AI options for your everyday workflow. Since then, we have enhanced the benchmark based on your feedback, including evaluating <a href="https://x.com/AndroidDev/status/2064482677500080549">open-weight models</a> and adding cost and efficiency dimensions to the leaderboard.</p>

<p>But AI capabilities are ever-evolving, and measurement needs to follow suit. As part of our July release, we have adopted the <a href="https://www.harborframework.com/">Harbor framework</a>, which includes an updated version of the benchmarking agent used to evaluate models.</p>

Along with this change to our evaluation, in this July release we’re adding 8 new models (<b>Claude Fable 5, Claude Sonnet 5, Claude Opus 4.8, GLM 5.2, Kimi K2.7 Code, MiniMax M3, Qwen 3.7 Plus and Qwen 3.7 Max</b>) to the leaderboard. We’re also sharing opportunities for you, the Android developer community, to contribute to the benchmark.

<h2 style="margin-top: 10px;">Upgrading our methodology with the Harbor framework</h2>

<p>When we designed Android Bench, we anchored our methodology on leading industry standards available at the time. We used mini-swe-agent v1, a general-purpose benchmarking agent, and adapted it to the nuances of Android development to provide a baseline measurement for the capabilities of models for common Android development tasks.</p>

<p>To continue providing you with state-of-the-art evaluations that accurately measure the latest model capabilities on Android development, we are standardizing our benchmark to the <a href="https://www.harborframework.com/">Harbor framework</a>. Harbor defines standards and integrations that make it easy for anyone to run the benchmark, evaluate their preferred set-up, or share results – providing you with additional transparency and visibility.</p>

<p>This upgrade enables us to more rigorously evaluate models and their capabilities, and we re-ran the benchmark on all models to establish an updated baseline. This means there is a minor shift in scoring, but you will still be able to view historical scores within <a href="http://d.android.com/bench/archive">the archive</a> on our website.</p>

<p>We want to ensure Android Bench is helpful for you, so we will continuously update it as our evaluations and the industry mature.</p>

<h2 style="margin-top: 10px;">Expanding the leaderboard with 8 new models</h2>

<p>As part of our commitment to keeping the leaderboard fresh, we have added Claude Fable 5, Claude Sonnet 5, Claude Opus 4.8, GLM 5.2, Kimi K2.7 Code, MiniMax M3, Qwen 3.7 Plus and Qwen 3.7 Max to the Android Bench leaderboard.</p>

<p>You will see that <b>Claude Fable 5</b> is at the top of the leaderboard with a score of 84.5, followed by <b>GPT 5.5</b> with 80.2, with <b>Claude Sonnet 5</b> in 3rd with a score of 76.2.</p>

<p>When just comparing Open-weight models,<b> GLM 5.2</b> is at the top with 72.2, followed by <b>Kimi K2.7 Code</b> with a score of 70.4.</p>

<p>You can check out model performance and efficiency metrics on the updated leaderboard to see how these new and previous models navigate Android-specific challenges like Jetpack Compose migrations, wearable networking, and platform API updates.</p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhQCbY3Td_I5gR8bC4uFSBTe4Sl-XuArNNdFU-27JP6-kwHycXt9AMpWfkLqjUIK37Zw18Tel6a7yOS9x0L_NabxBgYd9KIJKZ6dTLl6VxxJI4M7Zstqj12wvOFtF8LjnYrCIWnhCDdeGsgpQvFpFX8VOoSO0dFJcOW_gRc6eX7mXDq80sOwQAlQWNhlQg/s1999/image1.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="890" data-original-width="1999" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhQCbY3Td_I5gR8bC4uFSBTe4Sl-XuArNNdFU-27JP6-kwHycXt9AMpWfkLqjUIK37Zw18Tel6a7yOS9x0L_NabxBgYd9KIJKZ6dTLl6VxxJI4M7Zstqj12wvOFtF8LjnYrCIWnhCDdeGsgpQvFpFX8VOoSO0dFJcOW_gRc6eX7mXDq80sOwQAlQWNhlQg/s1600/image1.png" /></a></div>

<h2>Opening Android Bench to community contributions</h2>

<p>From the beginning, we’ve valued an open and transparent approach, which is why we made our original methodology and test harness publicly available on GitHub. You’ve asked for a way to provide feedback on our dataset, so now we’re taking collaboration a step further by giving you, the Android developer community, a chance to shape Android Bench.</p>

<p>Starting today, you can contribute to Android Bench in two ways:</p>

<ul>
    <li>Design and <a href="https://github.com/android-bench/community-dataset">submit your own Android development tasks</a> to evaluate how models handle the scenarios that matter to you.</li>
    <li><a href="https://github.com/android-bench/community-results">Run and share benchmark evaluations</a> firsthand, testing your preferred models against our dataset or your own custom tasks.</li>
</ul>

<p>We will be reviewing the submitted tasks and will be assessing if they get added to the benchmark. We hope to build a benchmark that truly reflects the diverse, day-to-day realities of the global Android developer community.</p>

<h2 style="margin-top: 10px;">Looking ahead</h2>

<p>With more and more options for agentic development, maintaining a cutting-edge benchmark ensures that the AI assistance you rely on keeps getting smarter, more helpful, and more effective. Head over to our <a href="https://github.com/android-bench/android-bench">GitHub repository</a> to check out the tasks. We invite you to submit a task to our team for review, and you can check out <a href="https://hub.harborframework.com/datasets/android-bench/android-bench/latest">Harbor Hub</a> to explore the dataset or submit evaluations.</p>

<p>As always, you can find the <a href="http://d.android.com/bench">updated leaderboard</a>, or read the <a href="http://d.android.com/bench/methodology">methodology</a> on our website.</p>
  <span style="display: none !important; visibility: hidden;">
    Android Bench, LLM leaderboard, Harbor framework, Android development, Claude Fable 5, GPT 5.5, Claude Sonnet 5, GLM 5.2, Kimi K2.7 Code, MiniMax M3, Qwen 3.7 Plus, Qwen 3.7 Max, AI benchmarking, Jetpack Compose migration, wearable networking, mobile AI agent, Zoe Lopez-Latorre, model evaluation, open-weight models, developer community contributions.
</span>
  </div></div>

### Eclipsa Video: HDR That Looks Right on Every Screen (Apple)
- **Published**: 2026-06-29T15:56:50.754-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/eclipsa-video-hdr-review.html](https://android-developers.googleblog.com/2026/06/eclipsa-video-hdr-review.html)
- **Key Topics**: AI-generated content requirements, App Review AI guidance
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhGg9E8BsBcgigJ3Pwhp0Wbd85wffhQKw9jT9eW4_IJHtJsxtaqBqZoWIc4agLIZu9h2eWFEnMgipcv2PnMM2UC9tsZOJp3AMjsOX1KQRoisg5IKTRS20hFOIvJmlViYFz-QOh3-KdyFRIgUaiKs2ehjrJBd9W_yW13aP4xgRQovNCEAviajCLWFTTVrjs/s2469/Eclipsa%20Video%20V01%20White_Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhGg9E8BsBcgigJ3Pwhp0Wbd85wffhQKw9jT9eW4_IJHtJsxtaqBqZoWIc4agLIZu9h2eWFEnMgipcv2PnMM2UC9tsZOJp3AMjsOX1KQRoisg5IKTRS20hFOIvJmlViYFz-QOh3-KdyFRIgUaiKs2ehjrJBd9W_yW13aP4xgRQovNCEAviajCLWFTTVrjs/s2469/Eclipsa%20Video%20V01%20White_Meta.png" style="display: none;" /><div><i>Posted by Tibian Elsheikh, Product Manager, Android Core Graphics and Jeffrey Jose, Product Manager, Android Core Graphics</i></div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg0slfG8CUVGmPiAUHIXkeIVZGveJMOvf1TorUdONiRYV1THM80OzIIjGV5-bOboEhNz7FB4sTYx72ySEjFhQ4oW97-sLZ4scOX2Sb5BBU9qPMvOXvq2XRj098K7ElBnvy4k68jKELpDZ7vd4NIs2Hud2w14re18dOx7dksdFXRBR_Nd8yOiBrw8cLr_kM/s8583/Eclipsa%20Video%20V02_Blog.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2601" data-original-width="8583" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg0slfG8CUVGmPiAUHIXkeIVZGveJMOvf1TorUdONiRYV1THM80OzIIjGV5-bOboEhNz7FB4sTYx72ySEjFhQ4oW97-sLZ4scOX2Sb5BBU9qPMvOXvq2XRj098K7ElBnvy4k68jKELpDZ7vd4NIs2Hud2w14re18dOx7dksdFXRBR_Nd8yOiBrw8cLr_kM/s1600/Eclipsa%20Video%20V02_Blog.png" /></a></div><br /><p><br /></p>
<p>We’ve all been there: You’re scrolling through your favorite social media feed in a dim room, and suddenly an HDR video pops up. It’s so intensely bright that you have to squint, or maybe you find yourself turning down your screen brightness just to read the caption. Other times, a video that looks vibrant on your phone looks flat, dark, or washed out when you watch it on your living room TV.&nbsp;</p><p>While High Dynamic Range (HDR) technology was designed to make videos look richer and more lifelike, the lack of unified industry guidelines means that the exact same clip can render in unexpected and jarring ways depending on the display you’re using.</p>

<p>To solve this, we’re introducing Eclipsa Video—a new standard built to make your favorite videos look consistent, balanced, and comfortable on every screen. Eclipsa Video builds on the open <a href="https://github.com/SMPTE/st2094-50">SMPTE ST 2094-50 specification</a>, which Google developed in collaboration with Apple and NBCUniversal.</p><br /><p></p><i><div style="text-align: center;"><i><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiLDY0gLjHQYTZZfRzikfPu8P3jZkXhq6Wqo1GFj3CvBh9YaboIDUstPcnV94Qan8nVkXXBlXLm5vSktLM_q9DJIIn_jyeW9LyZchI5Fpm6AD7A5XD3ZRslzBFhJLAvRj589ukW0etBNCg7004SjySw_SYsGkg6dQ8AtgfofOZeFTx8R3H7xWfwAuA-Rqc/s1066/Eclipsa_9-16_Transparent%20(2).gif" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1066" data-original-width="600" height="400" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiLDY0gLjHQYTZZfRzikfPu8P3jZkXhq6Wqo1GFj3CvBh9YaboIDUstPcnV94Qan8nVkXXBlXLm5vSktLM_q9DJIIn_jyeW9LyZchI5Fpm6AD7A5XD3ZRslzBFhJLAvRj589ukW0etBNCg7004SjySw_SYsGkg6dQ8AtgfofOZeFTx8R3H7xWfwAuA-Rqc/w225-h400/Eclipsa_9-16_Transparent%20(2).gif" width="225" /></a></div>Sudden brightness spikes during feed scrolling—fixed with Eclipsa Video.</i></div></i><p></p>

<h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">More consistency, comfort, and creative control</span></strong></h3>Eclipsa Video moves past individual display guesswork. Instead of leaving it up to your device to interpret a video’s brightness on its own, our format carries precise guidelines that tell compatible displays exactly how to render the image. <br /><p>Designed to scale with your hardware, Eclipsa Video provides three core benefits:</p>

<ul>
    <li><strong>A consistent baseline:</strong> Eclipsa Video introduces a shared rulebook for screens. It establishes a consistent benchmark for normal brightness—known as the <b>HDR reference white</b>. This ensures standard text, app interfaces, and standard-range colors remain vibrant and readable without causing uncomfortable screen glare.</li>
    <li><strong>Adaptive headroom:</strong> Screens have different physical brightness limits, or "headroom." Eclipsa Video guides how displays handle highlights dynamically. Bright details remain brilliant on a premium television, while being scaled intelligently on a mobile screen to prevent sudden blinding transitions.</li>
    <li><strong>Preserved creative intent:</strong> Rather than applying a single static setting to an entire video, Eclipsa Video carries adaptive, frame-by-frame instructions. Think of it as a set of digital notes from the creator traveling with the video, ensuring the exact colors, contrast, and mood they graded are preserved on your display.</li></ul>

<div class="separator" style="clear: both;"><img border="0" data-original-height="1080" data-original-width="2200" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEirgS5TsogRUxWbypUiFlWIRuL8nQhdagvc7UHVFjoDG00SjqSrMniKFEys-EzgcrHKi6Am5BrtALEs7px1oaaJ5ciaO7hP0_49i8RuD7uCckjW7jYWrSoFkDlob6dJhL42MPLiBQqAjaPMOMJDEjZjDgvVe0P28fw13RlMNSiMEAlx5XFXCr8o6L8SRo0/s1600/Eclpsa%20Blog%20post%20image-AlphaB.png" /><br /><div style="text-align: center;"><i>Eclipsa Video preserves true highlight detail on any screen you watch.</i></div></div><h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">Built natively into Android 17</span></strong></h3>

<p>Starting with Android 17, support for Eclipsa Video is built directly into the platform. This means a more comfortable, true-to-life HDR experience is coming natively to the phones, tablets, and TVs you rely on every day. The video you capture carries its creative intent with it, and the video you watch is shown exactly the way it was meant to be seen.</p>

<h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">Guidelines for developers &amp; creators</span></strong></h3>

<p>We’re inviting the developer and creator ecosystem to help build a more reliable HDR environment:</p>

<ul>
    <li><strong>Get started with implementation:</strong> Learn how to configure playback and capture in your apps with our <a href="https://developer.android.com/media/platform/integrate-eclipsa-video">official guide</a>.</li>
    <li><strong>ExoPlayer &amp; Media3 integration:</strong> Standard playback handling built directly into <a href="https://developer.android.com/media/media3/exoplayer">Jetpack Media3,</a> allowing ExoPlayer to support Eclipsa Video metadata automatically with no additional player configuration.</li>
    <li><strong>Explore open source tools:</strong> View and inspect <a href="https://github.com/SMPTE/st2094-50">SMPTE ST 2094-50</a> metadata and dynamic gain curves in real time using <a href="https://webmproject.github.io/hdr-explorer/">HDR Explorer</a>.</li>
</ul>

<h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">What’s next</span></strong></h3>

<p>Eclipsa Video is rolling out now, and you’ll see more apps and devices supporting it over time. Because it’s an open standard, any app developer or hardware manufacturer can integrate it to elevate the viewing experience.</p>

<p>Try out the new tools in Android 17, explore the open-source metadata, and let us know what you think on our developer channels. We can’t wait to see what you create.</p>

<h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">Notes &amp; Availability</span></strong></h3>
<p style="text-align: left;"><strong>1. Device Compatibility:</strong> Eclipsa Video playback and capture are supported natively on devices running Android 17 (API level 37) and above with HDR displays passing Eclipsa Compliance tests.</p>
<p style="text-align: left;"><strong>2. Developer Resources:</strong> The <a href="https://github.com/SMPTE/st2094-50">SMPTE ST 2094-50 Specification</a> is openly accessible for technical evaluation.</p>

### Expanded billing choice and lower fees on Google Play (Google Play)
- **Published**: 2026-06-24T10:19:34.133-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/play-expanded-billing.html](https://android-developers.googleblog.com/2026/06/play-expanded-billing.html)
- **Key Topics**: Google Play AI policies, AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgUB5FJxvJIARbdD14jKJu4Jg0uzjczgDxybt5NlviqF_vL91B0GzqNHTcURyCT1nUJgc22LmhvXBk_E2UOXvLqXN_dZfs0YrlbMrl3ZJ_CYcn4W4qoTUhU5k0Y8DhoXltMRMUGQN7uzj6pH4qV1dtRCR6tAKpjmH3Ys_94xqHgR6SfHMpAplFgz8ClGG8/s8533/Apps%20Experience_Play%20Blog%20MetadataCard__2048x1323.jpg" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgUB5FJxvJIARbdD14jKJu4Jg0uzjczgDxybt5NlviqF_vL91B0GzqNHTcURyCT1nUJgc22LmhvXBk_E2UOXvLqXN_dZfs0YrlbMrl3ZJ_CYcn4W4qoTUhU5k0Y8DhoXltMRMUGQN7uzj6pH4qV1dtRCR6tAKpjmH3Ys_94xqHgR6SfHMpAplFgz8ClGG8/s8533/Apps%20Experience_Play%20Blog%20MetadataCard__2048x1323.jpg" style="display: none;" /><p></p><p><i>Posted by Paul Feng, Vice President, Google Play Eng, Product, UX</i></p><p></p>

<p></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj0NArBxSwBOPGYLZKJ4BxhB3rjkTq6RrZ6XBJk2e57TVQ_mSCJ1nw5JAegk0dmX-MEW0ArHvvr2pX8zdXKuJjIXsTgDx7i9W-EoRtS0rHLeGPjMnOvryY2f02czLEBxANuCYYa9ryEr46_6xJ9PQNkHL1MWh-hEHwZAbCGYj-JcdCunZGva5WpFFHCtYA/s4210/Blogger%20Header%20asset%20-%204209%20x%201253%20px.jpg" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1254" data-original-width="4210" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj0NArBxSwBOPGYLZKJ4BxhB3rjkTq6RrZ6XBJk2e57TVQ_mSCJ1nw5JAegk0dmX-MEW0ArHvvr2pX8zdXKuJjIXsTgDx7i9W-EoRtS0rHLeGPjMnOvryY2f02czLEBxANuCYYa9ryEr46_6xJ9PQNkHL1MWh-hEHwZAbCGYj-JcdCunZGva5WpFFHCtYA/s16000/Blogger%20Header%20asset%20-%204209%20x%201253%20px.jpg" /></a></div><br /><br />At Google Play, we are committed to delivering the best possible experience to users, while ensuring developers have the tools and adaptability to succeed. Guided by this commitment, <a href="https://android-developers.googleblog.com/2026/03/a-new-era-for-choice-and-openness.html">earlier this year</a> we announced updates to our business model introducing more billing flexibility, lower fees, and new programs to help your business thrive. <br /><br />With some of these changes rolling out soon, the breakdown below outlines what is coming, where to find more information, key dates, and how to get started.

<h2>More billing flexibility</h2>

Google Play’s billing system safely, efficiently, and intuitively handles the complexities of taxes, compliance, and subscriptions across 195+ markets with 300+ local payment methods. However, we understand there are situations where your business needs more flexibility, and that's why we're offering you more options in how you handle digital commerce.<p></p><p></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEicLIK5NuRI6Rf-N_scGYqy-xAMyFOrJRo-nJOjqBYQW3Fizevf5Mk3mKnNRlJWdEWKKQ3oM_whpPuVOABM9Nf8bZwkfGQ_12p4mgQDvO40ornXa_1OxyP_4okmNfbcOyXdq47nx7o11Q_D7BRe5nRBGt2tNWFhe_eAEIgFC-kFdZH8K8j0gfeWZUAuS1Y/s8000/MM6_Offer%20alt%20billing.jpg" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="4500" data-original-width="8000" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEicLIK5NuRI6Rf-N_scGYqy-xAMyFOrJRo-nJOjqBYQW3Fizevf5Mk3mKnNRlJWdEWKKQ3oM_whpPuVOABM9Nf8bZwkfGQ_12p4mgQDvO40ornXa_1OxyP_4okmNfbcOyXdq47nx7o11Q_D7BRe5nRBGt2tNWFhe_eAEIgFC-kFdZH8K8j0gfeWZUAuS1Y/s16000/MM6_Offer%20alt%20billing.jpg" /></a></div><br /><p></p>

<br /><br />Building from existing programs, the new billing choice program is available to all developers globally who provide digital services or content to users within the United Kingdom and the European Economic Area, alongside programs in the United States. Following this initial phase, we will continue expanding availability to additional markets. You will find the global release schedule at the bottom of this post.<br /><br />Through these programs, developers can offer an alternative billing system or link users to their own website for purchases, alongside Google Play’s billing. You may also design your own choice screen in accordance with our UX guidelines, as an alternative to Google Play’s default version.<br /><br />Please find all the details in the <a href="https://support.google.com/googleplay/android-developer/answer/17161464">program page here</a>.

<h2>Lower, separate fees</h2>To enable this new level of flexibility, we're separating our service fee from the billing fee. This starts on June 30, 2026, beginning with the United States, European Economic Area, and United Kingdom.<br /><br />Regardless of whether you use Google Play's billing system, alternative billing, or external web links, the service fee starts at 10% on your first $1M (USD) in annual earnings. This 10% service fee also applies to all auto-renewing subscriptions. For all other transactions, the rates in the table below applies:<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjaTaAgjv7m9xtS4DS25hgDQ6oMIQWBw-GQ0bDMv4D_J-W5r7njfSvs7EnSwnJNIZ9oOIqW0w8KqoA4tTOQ2kC_l4K1YsrGt9Dp-4PFKBJGoACzfZPCjE2KBB0PGBjpaWBCguanfdhd-86iPZ3nDL_tZsk-lSYINiyQAreP8HKzBuShqq0BepijI3X6LT0/s8000/MM6%20rate%20card%20without%20border.jpg" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="4500" data-original-width="8000" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjaTaAgjv7m9xtS4DS25hgDQ6oMIQWBw-GQ0bDMv4D_J-W5r7njfSvs7EnSwnJNIZ9oOIqW0w8KqoA4tTOQ2kC_l4K1YsrGt9Dp-4PFKBJGoACzfZPCjE2KBB0PGBjpaWBCguanfdhd-86iPZ3nDL_tZsk-lSYINiyQAreP8HKzBuShqq0BepijI3X6LT0/s16000/MM6%20rate%20card%20without%20border.jpg" /></a></div><p></p><br /><br /><p><br /></p>

For other transactions, the service fee will be determined by whether the transacting user's install is new or existing relative to the regional rollout date:<div>&nbsp;

<ul>
  <li><b>New installs</b>:&nbsp;A transaction from a user whose first-time install or first update of the app from Google Play occurred on or after the date that the new fee structure launched in their region.</li>
  <li><b>Existing installs</b>:&nbsp;A transaction from a user whose first-time install or first update of the app from Google Play occurred before the date that the new fee structure launches in their market.</li></ul><div><br /></div>For transactions that use Google Play’s billing system, an additional billing fee applies. In the United States, United Kingdom, and the European Economic Area, the billing fee is set at 5%. We'll announce billing fee details for other markets soon. For transactions processed via alternative billing or external web links, the billing fee does not apply. <br /><br />Review<a href="https://support.google.com/googleplay/android-developer/answer/16954621?hl=en"> this Help Center article</a> to understand how these rates apply to your business.

<h2>Games Level Up and Apps Experience program guidelines</h2>We are also excited to announce even more opportunities for partners who deliver exceptional user experiences across the Android ecosystem: the revamped <a href="https://play.google.com/console/about/levelup/">Games Level Up</a> and the new <a href="https://play.google.com/console/about/programs/appsexperience/">Apps Experience</a> program. Detailed guidelines are now available on the respective program websites.<br /><br />Apps and games that meet all requirements are eligible for a new program rate card with reduced rates. See the table below for details:<p></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi6Zf6OFaB1B8MD7DeLJ-znJQUcA3ozQYDUEKzxiJb-32f_zk8bn6Cyi-WbwDPND0osW6FmmaUlfi1ji25thN3kZYXb747mD_KaE6pUf3faA5blqHNFH7qRlp0aNgVvS-bNNLg8L3QTizxXOU0mmblc8RyapiRanHcdocW92FchSLuJnw1HUSYbY2oJfNI/s8000/MM6%20rate%20card%20with%20border.jpg" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="4500" data-original-width="8000" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi6Zf6OFaB1B8MD7DeLJ-znJQUcA3ozQYDUEKzxiJb-32f_zk8bn6Cyi-WbwDPND0osW6FmmaUlfi1ji25thN3kZYXb747mD_KaE6pUf3faA5blqHNFH7qRlp0aNgVvS-bNNLg8L3QTizxXOU0mmblc8RyapiRanHcdocW92FchSLuJnw1HUSYbY2oJfNI/s16000/MM6%20rate%20card%20with%20border.jpg" /></a></div><br /><p></p>

Visit the <a href="https://play.google.com/console/about/levelup/">Games Level Up</a> and <a href="https://play.google.com/console/about/programs/appsexperience/">Apps Experience</a> program websites, review the guidelines, and start preparing your games and apps ahead of September 30, 2026, when the program rate cards officially become available.

<h2>Global release schedule</h2>

Evolving our business model requires technical infrastructure and alignment with local regulations, so these updates will roll out on a staggered timeline. To help you plan, here is the previously announced release schedule for each update across all markets:<p></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjIGtrW01aFRzy0gj7_mHMrJ1TrWHkan3S0aF7HmjhM3QGdpkb9xjJudKp02b6i3jGGjRyE7PYGVPwxIhrM4CdLs_A-P70ugCns-G5x05x3PnAqD7VweBHg7-06bUl4T98OPuGpEXjrAjbwMObraQn8K3uCnr3tr505Os8Keu3H_i4wbWaZNoixFv6_vYw/s8000/MM6%20Release%20Schedule.jpg" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="4500" data-original-width="8000" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjIGtrW01aFRzy0gj7_mHMrJ1TrWHkan3S0aF7HmjhM3QGdpkb9xjJudKp02b6i3jGGjRyE7PYGVPwxIhrM4CdLs_A-P70ugCns-G5x05x3PnAqD7VweBHg7-06bUl4T98OPuGpEXjrAjbwMObraQn8K3uCnr3tr505Os8Keu3H_i4wbWaZNoixFv6_vYw/s16000/MM6%20Release%20Schedule.jpg" /></a></div><br /><p></p>

<p>Here is a quick recap of the resources available to help you get started:</p>

<ul>
  <li>Review the <a href="https://support.google.com/googleplay/android-developer/answer/17161464"><b>billing choice program</b></a>;</li>
  <li>Learn more about <a href="https://support.google.com/googleplay/android-developer/answer/16954621?hl=en"><b>Google Play's lower service fees</b></a>;</li>
  <li>Explore detailed guidelines on the <a href="https://play.google.com/console/about/levelup/"><b>Games Level Up</b></a> and <a href="https://play.google.com/console/about/programs/appsexperience/"><b>Apps Experience</b></a> program websites.</li>
</ul>

<p>We look forward to building the next generation of Google Play experiences together.</p></div>

### Android developer verification: Building a safer ecosystem together (Google Play)
- **Published**: 2026-07-15T10:02:26.669-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/android-developer-verification.html](https://android-developers.googleblog.com/2026/06/android-developer-verification.html)
- **Key Topics**: Google Play AI policies, User safety requirements
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg2JeeSz9AeQDASycrf2ssGmJn2yQGvGFjyU29jKSs5hFtYySX9X5wDw4Pb63DF3co77osfiLeYj6LGt-_1v66X3svzCOdWAZz3w9Q2WKF28T4qZ4tCbiTEsP88lIZ44Ua6mLfg6VIQL_k3PVWlU4vDnJkTc9mJkdz188lH-smTL3oA47Yongl1w8sf4RY/s1235/260317_ADV%20Blog_Metadata.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg2JeeSz9AeQDASycrf2ssGmJn2yQGvGFjyU29jKSs5hFtYySX9X5wDw4Pb63DF3co77osfiLeYj6LGt-_1v66X3svzCOdWAZz3w9Q2WKF28T4qZ4tCbiTEsP88lIZ44Ua6mLfg6VIQL_k3PVWlU4vDnJkTc9mJkdz188lH-smTL3oA47Yongl1w8sf4RY/s1235/260317_ADV%20Blog_Metadata.png" style="display: none;" /><div><i>Posted by Matthew Forsythe, Director Product Management, Android App Safety</i></div><div><br /></div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg4_MWnkCTsO9zdnVQqFu2Aep5Q_GMvQvuXoGn-H_LXNpOYIVYFqbHi0R0iKpChOEJ-GB0p_7fLCiK_IGETshue4Fjd3tjyg95M3i92-DzdZpND5GPhr9jeBuj620YHAhPJ6CLdDXD8jsA1XyyYiBCS4p4eoZizZnA0DHKpwJqDUq-agwXl_GbtLrKdM5Y/s4210/260317_ADV%20Blog_Header.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1254" data-original-width="4210" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg4_MWnkCTsO9zdnVQqFu2Aep5Q_GMvQvuXoGn-H_LXNpOYIVYFqbHi0R0iKpChOEJ-GB0p_7fLCiK_IGETshue4Fjd3tjyg95M3i92-DzdZpND5GPhr9jeBuj620YHAhPJ6CLdDXD8jsA1XyyYiBCS4p4eoZizZnA0DHKpwJqDUq-agwXl_GbtLrKdM5Y/s16000/260317_ADV%20Blog_Header.png" /></a></div><br /><br /><div><br /></div><div><br /></div><div><br /></div><b>July 15, 2026: Updated Play Console requirements for Play developers</b><br /><br /><blockquote style="border-color: currentcolor; border-image: none; border-style: none; border-width: medium; margin: 0px 0px 0px 40px; padding: 0px; text-align: left;">To meet Android developer verification and <a href="https://support.google.com/googleplay/android-developer/answer/17125096">updated Play Console Requirements</a>, Play developers must <a href="https://support.google.com/googleplay/android-developer/answer/16984799">register their Play apps</a> in Play Console. While 99% of apps on Play have been registered automatically, you should check your <a href="https://play.google.com/console/u/0/developers/5700313618786177705/android-developer-verification">Play Console Home page</a> to register any remaining apps by September 30, 2026 to avoid global removal from Google Play and ensure a seamless user installation experience. </blockquote><br /><blockquote style="border-color: currentcolor; border-image: none; border-style: none; border-width: medium; margin: 0px 0px 0px 40px; padding: 0px; text-align: left;">You can also use Play Console to register apps you distribute outside of Google Play to ensure they can be installed on certified Android devices.</blockquote><span id="docs-internal-guid-afed0f58-7fff-2f52-4264-5e75e9454885"><div><br /></div></span><div>Last year, we introduced <a href="https://developer.android.com/developer-verification">Android developer verification</a> to strengthen ecosystem security and stop malicious actors from hiding behind anonymity to release harmful apps. Millions of apps have been registered since the verification launched in March, covering nearly all installs on Google Play and a large majority of installs from outside of Google Play. We appreciate the feedback and partnership from industry leaders, developers, and Android communities that helped us design this experience and drive strong adoption.<h2 style="margin-top: 12px;">Initial launch across seven stores and four countries</h2>

<p>These new developer verification protections will take effect on September 30, 2026, starting with users in Brazil, Indonesia, Singapore, and Thailand.</p>

<p>This rollout is an <b>industry-wide effort to create a safer ecosystem</b>. We will begin by verifying app installations from the following stores:</p>

<ul>
    <li>Google (Google Play)</li>
    <li>Honor (HONOR App Market)</li>
    <li>OPlus (OPPO App Market)</li>
    <li>Samsung (Galaxy Store)</li>
    <li>Transsion (Palm Store)</li>
    <li>vivo (V-Appstore)</li>
    <li>Xiaomi (GetApps)</li>
</ul>

<p style="margin-bottom: 4px;">Following this initial phase with our partners, we will expand these protections globally for all apps on certified Android devices in 2027.</p><h2 style="margin-top: 12px;">Automate your workflow with new APIs</h2>

<p>To further streamline app registration, we are<b> launching a suite of developer-requested APIs</b> to help you register apps in bulk or directly through your continuous integration and deployment (CI/CD) pipelines. The Android Developer ID Status API will let you check if a package name has already been registered, and the Android Developer Console API will let you register and manage package names directly within your development environment. Both APIs also support OAuth delegation, allowing third-party platforms, like Android app stores, to perform these operations natively on your behalf.</p>

We'll launch these APIs over the next few months.<h2 style="margin-top: 12px;">What’s next</h2>

<p></p><ul style="text-align: left;"><li><strong>June 2026:</strong> Starting this month, we are rolling out a new <a href="https://support.google.com/android/answer/17065026">system service</a> that will be automatically installed on most Android devices. This service will be used later this year to verify developer registration.</li><li><strong>July 2026:</strong> We’ll launch the Android Developer ID Status API globally and begin early access for the Android Developer Console API. Early access also starts for <a href="https://developer.android.com/developer-verification/guides/limited-distribution">limited distribution accounts</a> on Android Developer Console. This new type of Android developer account is designed for students, hobbyists, and learners and lets you share your apps to up to 20 devices without a government-issued ID or a fee.</li><li><strong>August 2026:</strong>&nbsp;Limited distribution accounts and the new Android Developer Console API will launch globally. We’ll also launch an <a href="https://android-developers.googleblog.com/2026/03/android-developer-verification.html">advanced flow</a> for installing apps from unverified developers, which includes security checkpoints to resist coercion scams, while allowing power users to maintain the ability to <a href="https://developer.android.com/developer-verification/guides/faq#sideload-apps">sideload apps</a> from unverified developers.</li><li><strong>September 30, 2026:</strong> App registration becomes required for <b>participating stores in Brazil, Indonesia, Singapore, and Thailand</b>. Unregistered apps can be sideloaded with Android Debug Bridge (adb) or advanced flow.</li><li><strong>2027 and beyond:</strong> After incorporating the feedback from our partners, users, and developer community, we’ll expand the Android verification requirement globally.<br /></li></ul><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhFUMAeS0ew75nme5xUK0qAQraK0-WpiUXp1B6m1yJFMqOrHUo7AyMMEfO-aYq9mZ6vy7GYPcBxRByKGQNgRbS99uW1b5hwbViEmIbGFVsLqhw7e-LSF_dozTAlKb7D1n_0Rc42S5MxzpxI5rrbSdDIQMVt6SXEErcnI-HrA0McFfL_BMoe2xMJtG9UU6I/s960/ABL_83_Blog%20in%20line%20asset%20-%20ADV%20July.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="540" data-original-width="960" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhFUMAeS0ew75nme5xUK0qAQraK0-WpiUXp1B6m1yJFMqOrHUo7AyMMEfO-aYq9mZ6vy7GYPcBxRByKGQNgRbS99uW1b5hwbViEmIbGFVsLqhw7e-LSF_dozTAlKb7D1n_0Rc42S5MxzpxI5rrbSdDIQMVt6SXEErcnI-HrA0McFfL_BMoe2xMJtG9UU6I/s1600/ABL_83_Blog%20in%20line%20asset%20-%20ADV%20July.png" /></a></div><br /><div><br /></div><h2 style="margin-top: 12px;">Get started with Android developer verification</h2>

<p>If you distribute apps in Brazil, Indonesia, Singapore, or Thailand via the stores listed above, please ensure your verification is complete by the September deadline.</p>

<p></p><ul style="text-align: left;"><li><strong>Google Play developers:</strong> Most Play developers are already verified, and over 99% of their apps have been registered. Go to your <a href="https://play.google.com/console/developers/app-list">Play Console Home page</a> to see your app’s verification status, and <a href="https://support.google.com/googleplay/android-developer/answer/16984799">register apps</a> you want to continue distributing that weren't automatically registered.</li><li><strong>Developers who distribute only outside of Google Play:</strong>&nbsp;Sign up for the <a href="https://android.google.com/developerconsole/developers">Android Developer Console</a> today to register your apps.</li></ul><p></p>



<p></p><ul style="text-align: left;"><ul><li><strong>Students and hobbyists:</strong>&nbsp;Sign up <a href="https://google.qualtrics.com/jfe/form/SV_4N7NGE06NjJJdl4">here</a> for early access to limited distribution accounts to help us refine the feature with your feedback.</li></ul></ul><p></p>

Thank you for helping us build a safer Android ecosystem. Stay tuned for more updates as we approach September and the 2027 global rollout.</div>

### Building a Mixed-Reality Tour Guide with Android XR, the Geospatial API, and Gemini (Google Play)
- **Published**: 2026-07-16T09:53:34.323-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/android-xr-geospatial-api-gemini.html](https://android-developers.googleblog.com/2026/06/android-xr-geospatial-api-gemini.html)
- **Key Topics**: AI-generated content disclosures, User safety requirements
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjKrortZT9X64_5gun79eaNo1niWelmj6Mixfrw4eBLKkec02_w-el6vVXR8IuyPA40B4lB22yEdCK5KNVOZ3DwG3sja7MJArx60irN7gP9P7rnzMjx8sejJeE6puifztBfMv_mExAuAjKkE3rjW1PRulfU0wTfIVLtmb9lEUW4L9hhFme1ArGmV09GuXM/s320/MM%20Android%20XR%20Geospatial%20V02_Meta%20(1).png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjKrortZT9X64_5gun79eaNo1niWelmj6Mixfrw4eBLKkec02_w-el6vVXR8IuyPA40B4lB22yEdCK5KNVOZ3DwG3sja7MJArx60irN7gP9P7rnzMjx8sejJeE6puifztBfMv_mExAuAjKkE3rjW1PRulfU0wTfIVLtmb9lEUW4L9hhFme1ArGmV09GuXM/s320/MM%20Android%20XR%20Geospatial%20V02_Meta%20(1).png" style="display: none;" /><div><i>Posted by Coco Fatus, UX Designer, Alon Hetzroni, UX Engineer, Azin Mehrnoosh, Product Manager Android XR</i></div><div><i><br /></i></div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgTa2M7znb9EjsONU5iM1tvB_KPswY-yT7pqYZ2gZmJGk9Z6WONXgDOsTj9vvTPD8a38-XvPm7HafuF1-nChC7dix2CQfnTpH6T-YdPhaL85A7rRugnlwwtPtwH-Z5WWSFVNYXCclOOL5DtNbNqRLX-ZJVAIrRDxYs8pgfWS0O0O2P_e-W6TjYH_RjnCuM/s8000/MM%20Android%20XR%20Geospatial%20V02_Blog.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2442" data-original-width="8000" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgTa2M7znb9EjsONU5iM1tvB_KPswY-yT7pqYZ2gZmJGk9Z6WONXgDOsTj9vvTPD8a38-XvPm7HafuF1-nChC7dix2CQfnTpH6T-YdPhaL85A7rRugnlwwtPtwH-Z5WWSFVNYXCclOOL5DtNbNqRLX-ZJVAIrRDxYs8pgfWS0O0O2P_e-W6TjYH_RjnCuM/s16000/MM%20Android%20XR%20Geospatial%20V02_Blog.png" /></a></div><br /><div><br /><br /><i><br /></i><div><i><br /></i><p><a href="https://www.youtube.com/watch?v=1KOO2lqsdaA">At this year's Google I/O</a>, we announced an update for spatial experiences: the <a href="https://developer.android.com/reference/kotlin/androidx/xr/arcore/Geospatial">Geospatial API</a> is now available as a preview in <a href="https://developer.android.com/develop/xr/jetpack-xr-sdk/arcore">ARCore for Jetpack XR</a>. By bringing Google's Visual Positioning System (VPS) to Android XR, Android XR enables anchoring digital content to the physical world with sub-meter accuracy and precise orientation in supported areas.* To explore what the Geospatial API could unlock, our team built a demo: the XR Geospatial Tour.</p>

<p>Imagine walking into a new city, putting on a pair of wired XR glasses (like the upcoming XREAL Project Aura), and instantly having a knowledgeable, local guide showing you around. You don't need to stare down at a 2D map—instead, 3D models gently guide your path, and an intelligent voice tells you about the historical landmarks right in front of you. We combined the <a href="https://developer.android.com/reference/kotlin/androidx/xr/arcore/Geospatial">Geospatial APIs</a>, <a href="https://firebase.google.com/docs/ai-logic">Gemini API using Firebase AI Logic</a>, <a href="https://ai.google.dev/gemini-api/docs/maps-grounding">Google Maps Grounding</a>, and <a href="https://developer.android.com/develop/xr/jetpack-xr-sdk">Jetpack XR SDK</a> to create a hands-free, immersive walking tour experience.</p>

<div class="separator" style="clear: both; text-align: center;"><iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/HpQLXX19boI" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="HpQLXX19boI"></iframe>

<p style="font-size: 0.85em; font-style: italic; line-height: 1.5; margin: 0px 0px 24px;">*Disclaimer: Video and Tour Guide application are for demonstration purposes only. Some sequences have been shortened. Any hardware depicted may be under development; final product details may differ.</p>

<p style="text-align: left;">Let’s walk through the implementation details and show how we tied these APIs together to build a world-scale spatial experience.</p>

<h3 style="text-align: left;">1. Pinpointing the User with ARCore Geospatial API (VPS)</h3>
<p style="text-align: left;">Enhance your navigation experience on XR by combining the power of GPS with the precision of VPS. The accuracy and precise orientation that comes with VPS allows 3D waypoints to align with the physical world.</p>

<p style="text-align: left;">This is why the Geospatial API on Android XR can help you build custom experiences. By using advanced computer vision, VPS tries to provide a <a href="https://developer.android.com/reference/kotlin/androidx/xr/runtime/math/GeospatialPose">GeospatialPose</a> (including latitude, longitude, and heading) that is more accurate than GPS.</p>

<p style="text-align: left;">Here's how we retrieve the user's Geospatial pose by mapping the device's orientation to a Geospatial coordinate:</p>
<pre><div style="text-align: left;">// Retrieve the current geospatial pose from the ARCore session</div><code><div style="text-align: left;">val result = geospatial.createGeospatialPoseFromPose(arDevice.state.value.devicePose)</div><div style="text-align: left;">if (result is CreateGeospatialPoseFromPoseSuccess) {</div><div style="text-align: left;">    val pose = result.pose</div><div style="text-align: left;">    Log.d("VPS", "Accurate Location: ${pose.latitude}, ${pose.longitude}")</div><div style="text-align: left;">}</div></code></pre>

<p style="text-align: left;">Because the entire experience relies on this accuracy, we monitor the horizontalAccuracy and orientationYawAccuracy until they meet our thresholds. If the user is indoors or in an unrecognized area, we prompt them to "walk to an outdoor public space and look around".</p>

<h3 style="text-align: left;">2. Crafting the Itinerary with Gemini API &amp; Google Maps Grounding</h3>
<p style="text-align: left;">Once we have a location, we use the <a href="https://firebase.google.com/docs/ai-logic">Gemini API using Firebase AI Logic</a> to prompt the Gemini model to act as a local tour guide. We pass the user's coordinates to the model and ask it to output a structured JSON response containing nearby walking tours:</p>

<pre><div style="text-align: left;">   val configForTools = ToolConfig(</div><code><div style="text-align: left;">      functionCallingConfig = null,</div><div style="text-align: left;">      retrievalConfig = retrievalConfig {</div><div style="text-align: left;">        latLng = FirebaseLatLng(pose.latitude, pose.longitude)</div><div style="text-align: left;">        languageCode = "en"</div><div style="text-align: left;">      }</div><div style="text-align: left;">    )</div><div style="text-align: left;"></div><div style="text-align: left;">    val responseJsonSchema = Schema.obj(</div><div style="text-align: left;">      mapOf(</div><div style="text-align: left;">        "locationIntro" to Schema.string(),</div><div style="text-align: left;">        "tours" to Schema.array(</div><div style="text-align: left;">          Schema.obj(</div><div style="text-align: left;">            mapOf(</div><div style="text-align: left;">              "title" to Schema.string(),</div><div style="text-align: left;">              "description" to Schema.string(),</div><div style="text-align: left;">              "stops" to Schema.array(</div><div style="text-align: left;">                Schema.obj(</div><div style="text-align: left;">                  mapOf(</div><div style="text-align: left;">                    "name" to Schema.string(),</div><div style="text-align: left;">                    "detailedName" to Schema.string(),</div><div style="text-align: left;">                    "description" to Schema.string()</div><div style="text-align: left;">                  )</div><div style="text-align: left;">                )</div><div style="text-align: left;">              )</div><div style="text-align: left;">            )</div><div style="text-align: left;">          )</div><div style="text-align: left;">        )</div><div style="text-align: left;">      )</div><div style="text-align: left;">    )</div><div style="text-align: left;"></div><div style="text-align: left;">    val model = Firebase.ai(backend = GenerativeBackend.googleAI()).generativeModel(</div><div style="text-align: left;">      modelName = "gemini-3.5-flash",</div><div style="text-align: left;">      tools = listOf(Tool.googleMaps()),</div><div style="text-align: left;">      generationConfig = generationConfig {</div><div style="text-align: left;">        responseMimeType = "application/json"</div><div style="text-align: left;">        responseSchema = responseJsonSchema</div><div style="text-align: left;">      }</div><div style="text-align: left;">    )</div><div style="text-align: left;"></div><div style="text-align: left;">   val result = model.generateContent("The user is at latitude ${pose.latitude} and longitude ${pose.longitude}. Generate exactly 3 diverse tours near this location (e.g., historical, food, nature). All tour ideas should be walking distance only.")</div></code></pre>

<p style="text-align: left;">Large Language Models are great at generating rich descriptions, but they can sometimes hallucinate exact latitude/longitude coordinates. To solve this, we used <a href="https://ai.google.dev/gemini-api/docs/maps-grounding">Google Maps Grounding</a> to ground the AI.</p>

<h3 style="text-align: left;">3. A Voice to Guide You: Gemini 2.5 TTS</h3>
<p style="text-align: left;">To make the tour guide feel truly present, we implemented dynamic voiceovers.</p>

<p style="text-align: left;">Using the gemini-2.5-flash-tts model, we can configure our model generation config to natively return audio data instead of just text! Here’s how you can request the ResponseModality.AUDIO:</p>

<pre><div style="text-align: left;">val ttsModel = Firebase.ai(backend = GenerativeBackend.googleAI())</div><code><div style="text-align: left;">    .generativeModel(</div><div style="text-align: left;">        modelName = "gemini-2.5-flash-tts",</div><div style="text-align: left;">        generationConfig = generationConfig {</div><div style="text-align: left;">            // Instruct the model to return Audio</div><div style="text-align: left;">            responseModalities = listOf(ResponseModality.AUDIO)</div><div style="text-align: left;">        }</div><div style="text-align: left;">    )</div><div style="text-align: left;"></div><div style="text-align: left;">val response = ttsModel.generateContent("Say in a neutral but positive voice:\n$prompt")</div><div style="text-align: left;"></div><div style="text-align: left;">// Extract the raw audio bytes from the response</div><div style="text-align: left;">val audioBytes = response.candidates.firstOrNull()?.content?.parts</div><div style="text-align: left;">    ?.filterIsInstance&lt;InlineDataPart&gt;()</div><div style="text-align: left;">    ?.firstOrNull { it.mimeType.contains("audio") }?.inlineData</div></code></pre>

<h3 style="text-align: left;">4. Bringing it to Life in 3D with Jetpack XR</h3>
<p style="text-align: left;">The final piece of the puzzle is rendering this data in the user's field of view. The Jetpack XR SDK makes it intuitive to transition from  a 2D Android UI to spatial computing.</p>

<p style="text-align: left;">We used Jetpack Compose for XR to build spatial components. To represent points of interest along the tour, we built a Composable called InfoSphere, which contains a GltfModel of a 3D orb that floats in space and can be interacted with to reveal information.</p>

<p style="text-align: left;">Using Jetpack XR SDK, we can place 3D models alongside the Compose UI using <a href="https://developer.android.com/reference/kotlin/androidx/xr/compose/subspace/SpatialBox.composable">SpatialBox</a> and <a href="https://developer.android.com/reference/kotlin/androidx/xr/compose/subspace/SceneCoreEntity.composable">SceneCoreEntity</a>. We also used <a href="https://developer.android.com/reference/androidx/xr/scenecore/InteractableComponent">InteractableComponent</a> to respond to user taps.</p>
<pre><div style="text-align: left;">@Composable</div><code><div style="text-align: left;">fun InfoSphere(</div><div style="text-align: left;">    content: InfoBubbleContent,</div><div style="text-align: left;">    session: Session,</div><div style="text-align: left;">    sphereModel: GltfModel,</div><div style="text-align: left;">    isSelected: Boolean,</div><div style="text-align: left;">    onClick: () -&gt; Unit</div><div style="text-align: left;">) {</div><div style="text-align: left;">    // SpatialBox lets us arrange 3D components and SpatialPanels together</div><div style="text-align: left;">    SpatialBox(</div><div style="text-align: left;">        SubspaceModifier</div><div style="text-align: left;">            .offset(x = 2.dp, y = 1.dp, z = (-3).dp) // Positioned in 3D space</div><div style="text-align: left;">    ) {</div><div style="text-align: left;">        // Smoothly animate the visibility of our 2D Compose UI Panel</div><div style="text-align: left;">        AnimatedSpatialVisibility(visible = isSelected) {</div><div style="text-align: left;">            SpatialPanel {</div><div style="text-align: left;">                InfoBubble(content) // Regular 2D Compose UI</div><div style="text-align: left;">            }</div><div style="text-align: left;">        }</div><div style="text-align: left;">        // Render our interactive 3D sphere</div><div style="text-align: left;">        SceneCoreEntity(</div><div style="text-align: left;">            factory = {</div><div style="text-align: left;">                GltfModelEntity.create(session, sphereModel).also { entity -&gt;</div><div style="text-align: left;">                    // Make the 3D model respond to user taps</div><div style="text-align: left;">                    entity.addComponent(InteractableComponent.create(session) { inputEvent -&gt;</div><div style="text-align: left;">                        if (inputEvent.action == InputEvent.Action.UP) {</div><div style="text-align: left;">                            onClick()</div><div style="text-align: left;">                        }</div><div style="text-align: left;">                    })</div><div style="text-align: left;">                }</div><div style="text-align: left;">            }</div><div style="text-align: left;">        )</div><div style="text-align: left;">    }</div><div style="text-align: left;">}</div></code></pre>

<p style="text-align: left;">By combining <a href="https://developer.android.com/reference/kotlin/androidx/xr/compose/subspace/animation/AnimatedSpatialVisibility.composable">AnimatedSpatialVisibility</a> for traditional Compose UI surfaces with SceneCoreEntity 3D elements, we're able to seamlessly blend data into the physical world.</p>

<h3 style="text-align: left;">Explore what’s possible with Android XR today</h3>
<p style="text-align: left;">Building the XR Geospatial Tour app showed us that the barrier to entry for world-scale spatial experiences is lower than ever for Android developers. With the Geospatial API now available in preview on Android XR, your apps can seamlessly understand the physical world around them. By combining <a href="https://developer.android.com/develop/xr/jetpack-xr-sdk/ui-compose">Compose for XR</a>’s APIs with the high-precision location data of VPS and the generative capabilities of Gemini, we can create experiences that understand both where the user is and what they are looking at.</p>

<p style="text-align: left;">To help you get hands-on with Android XR, we are thrilled to open applications for the <a href="https://developer.android.com/develop/xr/catalyst">Android XR Developer Catalyst Program</a>, which includes XREAL Project Aura. Starting today, you can apply to get access to an XREAL Project Aura devkit or our display glasses devkit over the coming months! </p>

<footer style="font-size: 0.85em; font-style: italic; line-height: 1.5; margin-top: 35px;">
  <p style="margin: 0px 0px 8px; text-align: left;">*Disclaimer: Available on select devices. Internet connection required. Works on compatible apps and surfaces. Results may vary.</p>
  <p style="margin: 0px;"><br /></p>
</footer></div></div></div>

### Android 17 is here (Google Play)
- **Published**: 2026-06-16T12:44:08.241-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/Android-17.html](https://android-developers.googleblog.com/2026/06/Android-17.html)
- **Key Topics**: Google Play AI policies, AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgV7zuuXjulHty999mGDWY1kfL8Q9SXjYYWn-7JTpMfVdNP78eb5fW9shOpvVdEqK0WnNp7AhdO0qc7pXAaqcfTwXgOGsfZyqcQv8wyD-9niWBpZuP6ZAPHBSetWenN2lMlRS5wi2d71-n8RCYqrLsFhUCEvM7KeoGLnNaDbiyOZQ0vvyr0O580nXK4Vas/s2048/Metadata%20-%20Static.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgV7zuuXjulHty999mGDWY1kfL8Q9SXjYYWn-7JTpMfVdNP78eb5fW9shOpvVdEqK0WnNp7AhdO0qc7pXAaqcfTwXgOGsfZyqcQv8wyD-9niWBpZuP6ZAPHBSetWenN2lMlRS5wi2d71-n8RCYqrLsFhUCEvM7KeoGLnNaDbiyOZQ0vvyr0O580nXK4Vas/s2048/Metadata%20-%20Static.png" style="display: none;" /><div><i>Posted by Matthew McCullough, VP of Product Management, Android Developer</i></div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg5KPJZylMSUXRpKFRUd6oM4fNdEoDRdJzdkzg69P_BVUuIDtXqCqTid6hGH40CoHRw7-f50HsT6rISArklGH982MM4K1jKU16SSymes4JPoE4qOZ5s1lLnkbInpUpdJGu5erAYmSgiefzkkOX_ng3AUJKOzzwC1WMTjk2DxLNia8R1C-ErWc7jT4VP8ew/s4209/Blogger%20Hero%20-%20White.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg5KPJZylMSUXRpKFRUd6oM4fNdEoDRdJzdkzg69P_BVUuIDtXqCqTid6hGH40CoHRw7-f50HsT6rISArklGH982MM4K1jKU16SSymes4JPoE4qOZ5s1lLnkbInpUpdJGu5erAYmSgiefzkkOX_ng3AUJKOzzwC1WMTjk2DxLNia8R1C-ErWc7jT4VP8ew/s16000/Blogger%20Hero%20-%20White.png" /></a></div><br /><p><br /></p><p>Today we're releasing Android 17 and making it available on most supported Pixel devices. Look for new devices running Android 17 in the coming months.</p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhjaHGBWXu3yvdXZ-wYQgN6DjN5TEMRIYDJvQDZTOybRZFWsAMhqhl14b9UZmrlXlEIRDioqRc8m3xRjOnQHJPoICkVpCho4qrmKihPbu_SB7dGVNKwlAaX6eWdjLF4VUdGyzGfxtW0ziFggj63e778VVo38qpMKar4E1wuw0MiPCBvBdrTTXCgI1XD04Q/s1080/AfD-Android-17.gif" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1080" data-original-width="1080" height="320" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhjaHGBWXu3yvdXZ-wYQgN6DjN5TEMRIYDJvQDZTOybRZFWsAMhqhl14b9UZmrlXlEIRDioqRc8m3xRjOnQHJPoICkVpCho4qrmKihPbu_SB7dGVNKwlAaX6eWdjLF4VUdGyzGfxtW0ziFggj63e778VVo38qpMKar4E1wuw0MiPCBvBdrTTXCgI1XD04Q/s320/AfD-Android-17.gif" width="320" /></a></div>

<p>Android 17 marks the start of our transition to an intelligence system, putting your apps at the center. It's shifting to an adaptive-first development standard by introducing mandatory large-screen resizability, all while delivering next-generation privacy, security, media, camera, and performance. We'll cover all that in this post, as well as how we're bringing together next generation tools, libraries, and agent skills to help your apps embrace the opportunity.</p>

<p>Throughout the past year, from our Canary channel to our Beta releases, we’ve collaborated with you in the developer community to build a platform you and your users can trust. To that end, this moment marks the availability of the source code at the <a href="https://source.android.com/">Android Open Source Project</a> (AOSP). This allows you to <a href="https://cs.android.com/">examine the source code</a> for a deeper understanding of how Android works.</p>

<p>Let's dive deeper into Android 17.</p>

<h3>An intelligence system</h3>

<p>With deep integration between hardware, software and AI, we’re transforming Android from an operating system to an intelligence system. It's about delivering new helpful experiences that anticipate user needs, and it brings more opportunities for engagement with your apps. To that end, Android 17 expands the capabilities of AppFunctions, a platform API with a corresponding Jetpack library. It allows you to contribute your app's unique capabilities as orchestratable "tools" for Android MCP, the on-device equivalent of the <a href="https://modelcontextprotocol.io/">Model Context Protocol</a>. AI agents and assistants (like Google Gemini) can discover and execute AppFunctions to perform workflows on behalf of the user with direct access to the app's local state.</p>

<p>The Jetpack library, currently in alpha, makes adding AppFunctions as easy as annotating a class and adding KDoc comments.</p>

<pre><code>/**
 * A note app's [AppFunction]s.
 */
class NoteFunctions(
    private val noteRepository: NoteRepository
) {
    /**
     * Adds a new note to the app.
     *
     * @param appFunctionContext The execution context.
     * @param title The title of the note.
     * @param content The note's content.
     */
    @AppFunction(isDescribedByKDoc = true)
    suspend fun createNote(
        appFunctionContext: AppFunctionContext,
        title: String,
        content: String
    ): Note {
        return noteRepository.createNote(title, content)
    }
}</code></pre>

<p>We’ve also launched an <a href="http://github.com/android/skills/tree/main/on-device/appfunctions">AppFunctions agent skill</a> that analyzes your app’s key workflows, automatically generates the required Kotlin code, optimizes your KDocs for LLM tool-calling, and provides ADB commands for testing and debugging.</p>

<p>The Gemini integration is currently in a private preview with trusted testers, but you can begin preparing your apps now. In addition to ADB commands to execute your AppFunctions, we've provided a <a href="http://github.com/android/appfunctions/releases/initial">test agent app</a> that includes an interface to discover and execute your app functions and simulate an AI agent integration. Join our integration early access program at <a href="http://goo.gle/eap-af">goo.gle/eap-af</a> for a chance to be among the first apps to deploy AppFunctions to production.</p>

<h3>Adaptive-first</h3>
<p>Your users no longer rely on a single form factor; they transition between phones, foldables, tablets, laptops, automotive displays, and immersive XR environments. Now, with over <a href="https://developer.android.com/blog/posts/adaptive-development-for-the-expanding-android-ecosystem">580 million large screen devices</a> in the hands of users and the <a href="https://blog.google/products-and-platforms/platforms/android/meet-googlebook/">forthcoming launch of Googlebooks</a>, the next generation of ChromeOS built on the Android stack, adaptive is no longer just a technical goal. It’s a massive opportunity to reach highly engaged users, which is one of the reasons we're shifting to an <a href="https://developer.android.com/adaptive-apps">adaptive-first development standard</a>.</p>

<h2>No resizability/orientation restrictions on large screens</h2>
<p>To ensure apps deliver a premium experience across all form factors, including mobile devices running in desktop mode on connected displays, Android 17 (API level 37) removes the developer opt-out for orientation and resizability restrictions on <a href="https://developer.android.com/guide/topics/large-screens">large screen devices</a> (sw &gt; 600 dp) for apps targeting API level 37. The system will ignore legacy manifest attributes and runtime APIs, including screenOrientation, setRequestedOrientation(), resizeableActivity=false, and aspect ratio constraints (minAspectRatio/maxAspectRatio). Games (based on <a href="https://support.google.com/googleplay/android-developer/answer/9859673?hl=en">app category</a> in Google Play) remain exempt. Your app must be ready to adapt to any window size, respect the user's preferred device posture, and support free-form windowing natively.</p>

<h2>Next-gen multitasking: App Bubbles, Bubble Bar, and desktop interactive PiP</h2>
<p>Android 17 introduces powerful new windowing capabilities that redefine how users multitask, demanding even greater layout flexibility from your apps:</p>
<ul>
    <li><strong>App Bubbles:</strong> Moving beyond the messaging bubbles API, users can now transform any app into a floating bubble by long-pressing its icon on the launcher. This feature is available across phones, foldables, and tablets, enabling lightweight multitasking for any workflow.</li>
    <li><strong>The Bubble Bar:</strong> On large screens (tablets and foldables), the system taskbar now includes a dedicated Bubble Bar to organize, transition between, and dock these floating app bubbles.</li>
    <li><strong>Desktop interactive PiP:</strong> In desktop environments, Android 17 introduces interactive Picture-in-Picture (PiP). Unlike traditional PiP windows which are read-only, these pinned windows remain fully interactive while staying always-on-top of other application windows.</li>
</ul>

<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg12FRQ31sUiyMj_ZalamTRI4VyI2tMXYKEoRy6b-u0Het272IDbRhznXot7b8AvFJEX-ubw_-pNxyS5JTKPUTBj1CNXwIYkTE906vembUcHeyGzE4Lb72WRyGNF7dOP_aBssNeCplOjEnKAc3d3hkak81LOpG0g9Hlep0AvC11MjdJ1MkqAp7ViUCu2bw/s1600/Bubbles%20(1).gif" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1600" data-original-width="1544" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg12FRQ31sUiyMj_ZalamTRI4VyI2tMXYKEoRy6b-u0Het272IDbRhznXot7b8AvFJEX-ubw_-pNxyS5JTKPUTBj1CNXwIYkTE906vembUcHeyGzE4Lb72WRyGNF7dOP_aBssNeCplOjEnKAc3d3hkak81LOpG0g9Hlep0AvC11MjdJ1MkqAp7ViUCu2bw/s16000/Bubbles%20(1).gif" /></a></div><p style="text-align: center;"><i>App Bubbles and Bubble Bar in action</i></p>

<h2>Activity recreation updates</h2>
<p>To prevent disruptive state loss and stutter, Android 17 updates the default behavior for Activity recreation. The system will no longer restart activities by default for typical configuration changes that do not require a full UI redraw (including <a href="https://developer.android.com/reference/kotlin/android/content/pm/ActivityInfo#config_keyboard">CONFIG_KEYBOARD</a>, <a href="https://developer.android.com/reference/kotlin/android/content/pm/ActivityInfo#config_keyboard_hidden">CONFIG_KEYBOARD_HIDDEN</a>, <a href="https://developer.android.com/reference/kotlin/android/content/pm/ActivityInfo#config_navigation">CONFIG_NAVIGATION</a>, <a href="https://developer.android.com/reference/kotlin/android/content/pm/ActivityInfo#config_touchscreen">CONFIG_TOUCHSCREEN</a>, and <a href="https://developer.android.com/reference/kotlin/android/content/pm/ActivityInfo#config_color_mode">CONFIG_COLOR_MODE</a>).<br />
Instead, running activities will receive these updates via onConfigurationChanged(), enabling smooth transitions. If your application explicitly relies on a full restart to reload resources for these changes, you must now explicitly opt-in using the new <a href="https://developer.android.com/reference/kotlin/android/R.attr#recreateonconfigchanges">android:recreateOnConfigChanges</a> manifest attribute.</p>

<h2>Continue On</h2>
<p>Android 17 adds Continue On to help users seamlessly transition a task between Android devices. The user sees a suggestion for the most recently opened app from their mobile device in their tablet taskbar, providing a one-tap affordance to launch the app and deep-link where they left off. Continue on can support app-to-web transitions, including falling back to using the web if the app isn't installed.</p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjc8K42DCZ0VTYpFhTlEazp9_AthhqYdm786k1NFolZrP7HwXk2QlF7UV1CU7ECK9N-CiHSfSbH_E2_cXwL3zUuesP-shpa1nau5QmVWDOQeErnCMtvZUw_wwAHNewZZ5S3811f0n_FNoX4U9kyptZQONM_eDB1AAHaoFjMFgTCC7G1d0X2iRo1MN8sev0/s1920/Continue%20On.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1200" data-original-width="1920" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjc8K42DCZ0VTYpFhTlEazp9_AthhqYdm786k1NFolZrP7HwXk2QlF7UV1CU7ECK9N-CiHSfSbH_E2_cXwL3zUuesP-shpa1nau5QmVWDOQeErnCMtvZUw_wwAHNewZZ5S3811f0n_FNoX4U9kyptZQONM_eDB1AAHaoFjMFgTCC7G1d0X2iRo1MN8sev0/s16000/Continue%20On.png" /></a><i>Handoff Suggestion on a Tablet</i></div><p style="text-align: left;"><br /></p>

<pre><code>class MyHandoffActivity : Activity() {

    ...

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    // Do stuff
    ...
    // Enable handoff
    setHandoffEnabled(true, null)
  }

  // Override and implement onHandoffActivityDataRequested
  override fun onHandoffActivityDataRequested(handoffRequestInfo: HandoffActivityDataRequestInfo) : HandoffActivityData {
    // Create and return handoff data
  }
}</code></pre>

<h2>Go adaptive-first with Jetpack Compose</h2>
<p>To help you adapt your apps to meet the new Android 17 requirements, we've launched the <a href="https://github.com/android/skills/tree/main/jetpack-compose/adaptive">Jetpack Compose adaptive skill</a>. This AI-powered developer workflow helps you implement the best adaptive practices:</p>
<ul>
    <li><strong>Adaptive navigation:</strong> Automatically transition between bottom navigation bars on mobile and edge-anchored navigation rails on large screens using NavigationSuiteScaffold from the Material 3 Adaptive library.</li>
    <li><strong>Multi-pane layouts:</strong> Implement list-detail and supporting pane layouts natively using Navigation 3 Scenes (ListDetailSceneStrategy and SupportingPaneSceneStrategy) instead of fragile fragment transactions.</li>
    <li><strong>FlexBox &amp; Grid APIs:</strong> Utilize Compose 1.11's dynamic layout components to easily adjust row and column spans on the fly, ensuring your content always fills the space beautifully.</li>
    <li><strong>Advanced non-touch input:</strong> Leverage Compose 1.11's enhanced trackpad and mouse support, including native focus rings and new APIs (like TrackpadInjectionScope and performTrackpadInput) to easily test and deliver a true "laptop-class" experience on Googlebooks and Desktop Mode.</li>
    <li><strong>Dynamic window states:</strong> Leverage Compose's reactive state model to seamlessly adapt your UI when the app transitions from full screen to a floating App Bubble or an interactive Desktop PiP window, ensuring a premium experience even at minimal dimensions.</li>
</ul>

<h2>Android is Compose-first</h2>
<p>Compose offers the easiest way to build adaptive apps, and that's just one of the <a href="https://developer.android.com/develop/ui/compose/first#why-compose-first">many reasons</a> we believe that all Android UI should be built with Compose. To that end, <a href="https://developer.android.com/develop/ui/compose/first">Android development is now Compose-first</a>. All new Android APIs, libraries, tools, and developer guidance will be built exclusively for Jetpack Compose. Legacy View components (in the android.widget package) and View-based Jetpack libraries (like Fragments, RecyclerView, and ViewPager) are now in maintenance mode. They will receive only critical bug fixes, and no new features.</p>

<blockquote>
    <p><strong>TIP</strong><br />
    Ready to migrate? Use our AI-driven <a href="https://developer.android.com/develop/ui/compose/migrate/migrate-xml-views-to-jetpack-compose">XML to Compose Migration Skill</a> to automatically analyze your legacy View layouts and convert them into highly-adaptive Compose code.</p>
</blockquote>

<h3>Performance &amp; efficiency</h3>
<p>App performance means a smooth user interface, fast app start times, and efficient multitasking; Android 17 has impactful improvements in all of these areas.</p>

<h2>App memory limits</h2>
<p>Memory usage is one of the silent foundations of overall performance. When a foreground app or service grows unchecked, memory management spikes CPU and battery utilization and eventually leads to the termination of other well-behaved cached apps and background jobs, ultimately forcing slower cold starts and impaired multitasking.&nbsp;</p>

<p>Starting in Android 17, the system will enforce strict app memory limits based on a device's total RAM, abruptly terminating offending processes. New things to help you navigate these tighter requirements:</p>
<ul>
    <li><strong>R8 Optimizer:</strong> The R8 optimizer significantly reduces your app's bytecode memory footprint by shrinking classes, methods, and fields into shorter names, and stripping out unused code and resources. Use R8 in full mode along with the new <a href="https://developer.android.com/topic/performance/app-optimization/r8-configuration-analyzer">R8 configuration analyzer</a> to make sure your app is getting the most from R8.<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiQePgjeISaotpA-miDPKel-qgAYtepLjMMBaiKZQqTf_iYRTJurn_iAFdC7utLnKRKAh9OhSjF_D83skA2PPg7xts0ORX7aVxBkoax6b9uEPqTlGiY_sh8Xv7U1pr0h4Nm8FLo-h3IJD8FhTJc-gOtpBwyLCnDBUPRJAuaaBjsIOhvUmTXFSna0ykksak/s2048/R8%20Configuration%20Analyzer.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="397" data-original-width="2048" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiQePgjeISaotpA-miDPKel-qgAYtepLjMMBaiKZQqTf_iYRTJurn_iAFdC7utLnKRKAh9OhSjF_D83skA2PPg7xts0ORX7aVxBkoax6b9uEPqTlGiY_sh8Xv7U1pr0h4Nm8FLo-h3IJD8FhTJc-gOtpBwyLCnDBUPRJAuaaBjsIOhvUmTXFSna0ykksak/s16000/R8%20Configuration%20Analyzer.png" /></a></div></li></ul><div><span style="color: #0000ee;"><u><br /></u></span></div><div><span style="color: #0000ee;"><u><br /></u></span></div><div><br /></div><div><br /></div><div style="text-align: center;">The R8 Configuration Analyzer</div><ul><li><strong>LeakCanary in Android Studio Panda:</strong> The profiler now features native LeakCanary integration as a dedicated task, fully integrated with your IDE and source code.</li>
    <li><strong>ApplicationExitInfo:</strong> If your app is terminated by these limits, getDescription() from ApplicationExitInfo will return "MemoryLimiter:AnonSwap".</li>
    <li><strong>On-Device Anomaly Detection:</strong> Part of ProfilingManager, you can leverage trigger-based profiling using TRIGGER_TYPE_ANOMALY to automatically capture heap dumps when the memory limit is reached.</li>
</ul>

<pre><code>val profilingManager = applicationContext
   .getSystemService(ProfilingManager::class.java)

val triggers = ArrayList&lt;ProfilingTrigger&gt;().apply {
  add(ProfilingTrigger.Builder(
    ProfilingTrigger.TRIGGER_TYPE_ANOMALY).build())
}
profilingManager.addProfilingTriggers(triggers)</code></pre>

<p>And, we're working to surface more in-field memory metrics to you within Google Play Console.</p>

<h2>Generational garbage collection</h2>
<p><a href="https://developer.android.com/about/versions">Android 17</a> introduces more frequent, less resource-intensive young-generation collections to <a href="https://developer.android.com/guide/platform#art">ART</a>'s Concurrent Mark-Compact garbage collector (GC). By separating short-lived objects from stable, long-lived ones, the system runs frequent, lightweight "young-generation" sweeps rather than expensive full-heap scans, drastically reducing CPU usage, power drain, and UI stutter. Our testing has shown significant improvements in GC interference with application threads and a reduction in the maximum memory resident set size (RSS). ART improvements are also available to over a billion devices running Android 12 (API level 31) and higher through Google Play System updates.</p>

<h2>Lock-Free MessageQueue</h2>
<p>For apps targeting SDK 37 or higher, the core <a href="https://developer.android.com/reference/android/os/MessageQueue"><b>android.os.MessageQueue</b></a> now implements a lock-free architecture, significantly reducing missed frames, improving app startup time, and radically improving the performance of busy queues in multithreaded scenarios. Note: This can break apps that use reflection on private <a href="https://developer.android.com/reference/android/os/MessageQueue"><b>MessageQueue</b></a> fields and methods.&nbsp; The <a href="https://developer.android.com/reference/android/os/TestLooperManager#peekWhen()"><b>peekWhen</b></a> and <b><a href="https://developer.android.com/reference/android/os/TestLooperManager#poll()">poll</a> </b>APIs have been added to <a href="https://developer.android.com/reference/android/os/TestLooperManager"><b>TestLooperManager</b></a> for instrumentation testing without relying on <a href="https://developer.android.com/reference/android/os/MessageQueue"><b>MessageQueue</b></a> internals.</p>

<h2>Static final fields now truly final</h2>
<p>Starting from Android 17, apps targeting SDK 37 or higher won’t be able to modify “static final” fields, allowing the runtime to apply performance optimizations more aggressively. An attempt to do so via reflection (or deep reflection) will lead to an IllegalAccessException being thrown. Modifying them via JNI’s <b><code>SetStatic&lt;Type&gt;Field</code></b> methods family will immediately crash the application.</p>

<h2>Custom notification view restrictions</h2>
<p>To reduce memory usage we are further restricting the size of <a href="https://developer.android.com/develop/ui/views/notifications/custom-notification">custom notification views</a>. This update closes a loophole that allows apps to bypass existing limits using URIs. This behavior is gated by the target SDK version and takes effect for apps targeting API 37 and higher.</p>

<h3>Privacy &amp; Security</h3>
<p>Maintaining user trust is at the heart of the Android ecosystem. Android 17 introduces robust features that protect sensitive data while simplifying user experiences.</p>

<h2>Privacy-preserving choices</h2>
<p>Historically, apps required broad, permanent permissions to access information like contacts, precise location and media files. Android 17 continues the shift toward privacy-preserving choices that grant temporary, session-based access only to the data the user explicitly selects:</p>
<ul>
  <li><strong>System-Level Contact Picker:</strong> Utilizing <code>ACTION_PICK_CONTACTS</code>, apps can request temporary access only to specific fields (e.g., email or phone number) chosen by the user, eliminating the need for the broad <code>READ_CONTACTS</code> permission. It also fully supports work/personal profile separation.</li>
    <li><strong>Customizable Photo Picker aspect ratio:</strong>&nbsp;Using<b><code>PhotoPickerUiCustomizationParams</code></b>, you can customize the system photo picker to show thumbnails in portrait mode. This is perfect for apps that always display photos and videos in portrait such as video based social media apps.</li>
    <li><strong>System-rendered Location Button:</strong> A new system-rendered location button that you can embed in your app grants precise location access for the current session only.</li>
    <li><strong>EyeDropper API:</strong> A new system-level API, <code>ACTION_OPEN_EYE_DROPPER</code>, allows your app to create a system-powered eyedropper enabling the user to select color from any pixel on the display. This provides a secure, privacy-preserving color-picking experience that eliminates the need for broad, sensitive screen capture or media projection permissions.</li>
</ul>

<pre><code>val eyeDropperLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result -&gt;
   if (result.resultCode == Activity.RESULT_OK) {
       val color = result.data?.getIntExtra(Intent.EXTRA_COLOR, Color.BLACK)
       // Use the picked color in your app
   }
}
fun launchColorPicker() {
   val intent = Intent(Intent.ACTION_OPEN_EYE_DROPPER)
   eyeDropperLauncher.launch(intent)
}</code></pre>

<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh8m_oR9WymjE9G26nGUCqdhS9GrBd6FXN3ujWbjq7ECD6OMGhS4xUApWkAWpPpRef7lwLhsRE2jYL9FADoF_FX2eMXD-0hp9JVaCzrDhfU8RYJ9qv-Ds9YIwyQK7yHKidW0oOtX1rpg2pG9x2yNp3UkGJDPqUlHX7hiLb-bvDue67FPZK1O-22SuXbO8I/s1267/Eyedropper%20Tester.webp" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="713" data-original-width="1267" height="360" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh8m_oR9WymjE9G26nGUCqdhS9GrBd6FXN3ujWbjq7ECD6OMGhS4xUApWkAWpPpRef7lwLhsRE2jYL9FADoF_FX2eMXD-0hp9JVaCzrDhfU8RYJ9qv-Ds9YIwyQK7yHKidW0oOtX1rpg2pG9x2yNp3UkGJDPqUlHX7hiLb-bvDue67FPZK1O-22SuXbO8I/w640-h360/Eyedropper%20Tester.webp" width="640" /></a></div><h3><br /></h3><h3><br /></h3><h3><br /></h3><h3><br /></h3><h3><br /></h3><h3><br /></h3><h3><br /></h3><h3><br /></h3><h3><br /></h3><h3 style="text-align: center;"><span id="docs-internal-guid-0ea8e748-7fff-dc26-5289-d5a9513c6997" style="font-weight: normal;"><span face="Arial, sans-serif" style="font-size: 11pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;"><i>Picking a color from anywhere on the screen with the system EyeDropper</i></span></span></h3><h2>Local network access</h2>
<p>Apps targeting Android 17 now either require the <code><a href="https://developer.android.com/reference/kotlin/android/Manifest.permission#access_local_network">ACCESS_LOCAL_NETWORK</a></code> runtime permission or the use of system-mediated, privacy-preserving device pickers for local network communication, such as talking to smart home devices or casting receivers. Because <code>ACCESS_LOCAL_NETWORK</code>  falls under the existing <code><a href="https://developer.android.com/reference/android/Manifest.permission_group#NEARBY_DEVICES">NEARBY_DEVICES</a></code> permission group, users who have already granted other <code><a href="https://developer.android.com/reference/android/Manifest.permission_group#NEARBY_DEVICES">NEARBY_DEVICES</a></code> permissions will not be prompted again. </p>

<h2>SMS OTP protection</h2>
<p>Android 17 expands SMS one-time-password (OTP) protection by delaying access to SMS messages for three hours:</p>
<ul>
  <li>WebOTP Format: <a href="https://developer.android.com/about/versions/17/behavior-changes-all#sms-otp-all-apps">Delayed for all apps that are not the intended recipient (domain mismatch)</a>.</li>
  <li>Standard SMS OTP: <a href="https://developer.android.com/about/versions/17/behavior-changes-17#sms-otp-protection">Delayed for all apps targeting SDK 37+</a>.</li>
  <li>Exemptions: Default SMS, assistant, and connected companion apps are exempt. Apps are strongly encouraged to migrate to the <a href="https://developer.android.com/identity/sms-retriever">SMS Retriever</a> or <a href="https://developers.google.com/identity/sms-retriever/user-consent/overview">SMS User Consent APIs</a>.</li>
</ul>

<h2>Post-Quantum Cryptography (PQC)</h2>
<p>Android 17 is ready for the next generation of cryptographic security:</p>
<ul>
  <li>Keystore Integration: Supported devices can generate ML-DSA (Module-Lattice-Based Digital Signature Algorithm) keys in secure hardware to produce quantum-safe signatures, exposed via standard JCA APIs.</li>
  <li>Hybrid APK Signing: Introducing the v3.2 APK Signature Scheme, which combines classical signatures with ML-DSA signatures to secure app delivery.</li>
</ul>

<h2>Safer native dynamic code loading&nbsp;</h2>
If your app targets SDK 37 or higher, the Safer Dynamic Code Loading (DCL) protection <a href="https://developer.android.com/about/versions/14/behavior-changes-14#safer-dynamic-code-loading">introduced in Android 14</a> for DEX and JAR files now extends to native libraries. All native files loaded using System.load must be marked as read-only. Otherwise, the system throws UnsatisfiedLinkError

<h2>Smarter password protection for physical inputs</h2>
<p>With Android 17, we're making it safer to enter passwords, PINs, and other secrets when using a physical keyboard by no longer showing the last typed character by default.</p>
<p>Users can still easily customize these display settings to match their preferences (availability may vary by device manufacturer).</p>
<p>These enhanced privacy protections are automatically supported byAndroid's built-in SDK components and will be supported in Compose 1.12 for SecureTextFields. </p>

<h3><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgFjWXyRLybiLVAIrIm1_60XHXhPmpB1QEph7AuqsGHs-NihIDRFbUgBh32gUKxo30173W-RpEInX9hmYFVnW5V8ZqtM3n_CzxlT0B0PVQr0LSOuOi7x2kZgN_jHRRlYJ7bYInZllvUGNoA_SrXkNi5wwHvUghUcnl0Gsgx_-ts4QEHq_KdbEYgWCg92xA/s798/Hide%20First%20Letter.gif" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="449" data-original-width="798" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgFjWXyRLybiLVAIrIm1_60XHXhPmpB1QEph7AuqsGHs-NihIDRFbUgBh32gUKxo30173W-RpEInX9hmYFVnW5V8ZqtM3n_CzxlT0B0PVQr0LSOuOi7x2kZgN_jHRRlYJ7bYInZllvUGNoA_SrXkNi5wwHvUghUcnl0Gsgx_-ts4QEHq_KdbEYgWCg92xA/s16000/Hide%20First%20Letter.gif" /></a></div></h3><h3><br /></h3><h3><br /></h3><h3><br /></h3><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><div><br /></div><i><div style="text-align: center;"><i>Smarter password protection for physical inputs</i></div></i><div><br /></div><h2 style="text-align: left;">Media and camera features that empower creators and delight users
</h2><p>Android 17 introduces new <a href="https://blog.google/products-and-platforms/platforms/android/android-17-creator-features/">creator features</a> that give access to pro-quality cameras and media, all while improving the experience for consumers.</p>

<ul>
  <li><a href="https://developer.android.com/media/platform/integrate-eclipsa-video">Eclipsa Video</a>: HDR video standard built upon the <a href="https://github.com/SMPTE/st2094-50">SMPTE ST 2094-50 specification</a> that introduces new metadata to help devices adapt content for their display headroom and ambient light conditions, as well as improve the simultaneous display of standard and HDR content.</li>
  <li>RAW14 image format: New support for the <a href="https://developer.android.com/reference/kotlin/android/graphics/ImageFormat#raw14">RAW14 image format</a> provides a way for your professional camera app to capture the highest level of detail and color depth from compatible camera sensors.</li>
  <li>Vendor-defined camera extensions: Vendor-defined extensions enable hardware partners to define and implement custom camera extension modes, providing access to the best and latest camera features.</li>
  <li>Extended HE-AAC software encoder: A new system-provided Extended HE-AAC software encoder, supports both low and high bitrates using unified speech and audio coding, providing significantly better audio quality for voice messages in low-bandwidth conditions, including support for loudness metadata.</li>
  <li><a href="https://developer.android.com/guide/topics/media/media-formats#video-formats">Versatile Video Coding (H.266)</a>:  Enables OEMs to add codec support by defining the <a href="https://developer.android.com/guide/topics/media/media-formats#video-formats">video/vvc</a> MIME type in <a href="https://developer.android.com/reference/android/media/MediaFormat"><code>MediaFormat</code></a>, adding new VVC profiles in <a href="https://developer.android.com/reference/android/media/MediaCodecInfo"><code>MediaCodecInfo</code></a>, and integrating support into <a href="https://developer.android.com/reference/android/media/MediaExtractor"><code>MediaExtractor</code></a>.</li>
  <li>Camera device type: New APIs that query the underlying device type to identify if a camera is built-in hardware, an external USB webcam, or a virtual camera.</li>
  <li>Constant Quality for Video Recording: <a href="https://developer.android.com/reference/android/media/MediaRecorder#setVideoEncodingQuality(int)"><code>SetVideoEncodingQuality</code></a> in <a href="https://developer.android.com/reference/android/media/MediaRecorder"><code>MediaRecorder</code></a> configures a constant quality (CQ) mode for video encoders to ensure uniform visual fidelity across the entire video.</li>
</ul>

<h2>Better support for hearing aids</h2>
<ul>
  <li>Bluetooth LE Audio hearing aid support: Android now includes a specific device category for Bluetooth Low Energy (BLE) Audio hearing aids with the new <a href="https://developer.android.com/reference/android/media/AudioDeviceInfo#TYPE_BLE_HEARING_AID"><code>AudioDeviceInfo.TYPE_BLE_HEARING_AID</code></a> constant, so your app can distinguish hearing aids from regular headsets to provide a tailored experience for users with assistive listening devices.</li>
  <li>Granular audio routing for hearing aids: Android 17 allows users to independently manage where specific system sounds are played. They can choose to route notifications, ringtones, and alarms to connected hearing aids or the device's built-in speaker, helping to avoid unwanted in-ear interruptions while maintaining a Bluetooth connection for hearing aid management apps.</li>
</ul>

<h2>CameraX and  Media3</h2>
<p><a href="https://developer.android.com/jetpack/androidx/releases/camerax">CameraX</a> and <a href="https://developer.android.com/jetpack/androidx/releases/media3">Media3</a> have been updated for Android 17. They are there to do the heavy lifting, smoothing the rough edges of media development and simplifying building reliable camera capture,  smooth media playback, and creative and complex editing experiences. </p>

<p>We've released an <a href="https://github.com/android/skills/tree/main/camera">agent skill</a> that can migrate legacy Android camera implementations (Camera1 or raw Camera2 APIs) to CameraX.</p>

<p>Note: You'll need to update your CameraX version to either 1.5.2 or 1.6.0+ to avoid a crash related to an added dynamic range mode on Android 17 devices.</p>

<h3>Get your apps, libraries, tools, and game engines ready!</h3>
<p>If you develop an Android SDK, library, tool, or game engine, it's critical to prepare any necessary updates now to prevent your downstream app and game developers from being blocked by compatibility issues and allow them to target the latest SDK features. Please let your downstream developers know if updates are needed to fully support Android 17.</p>

<p>Testing involves installing your production app or a test app making use of your library or engine using Google Play or other means onto a device or emulator running Android 17 Beta 4. Work through all your app's flows and look for functional or UI issues. Each release of Android contains platform changes that improve privacy, security, and overall user experience; review the app impacting behavior changes for apps <a href="https://developer.android.com/about/versions/17/behavior-changes-all">running on</a> and <a href="https://developer.android.com/about/versions/17/behavior-changes-17">targeting</a> Android 17 to focus your testing, including the following:</p>
<ul>
  <li>Resizability on large screens: Once you target Android 17 (SDK 37), you can no longer opt out of maintaining orientation, resizability and aspect ratio constraints <a href="https://developer.android.com/about/versions/17/changes/ff-restrictions-ignored">on large screens</a>.</li>
  <li>Dynamic code loading: If your app targets SDK 37 or higher, the Safer Dynamic Code Loading (DCL) protection <a href="https://developer.android.com/about/versions/14/behavior-changes-14#safer-dynamic-code-loading">introduced in Android 14 </a>for DEX and JAR files now extends to native libraries. All native files loaded using System.load() must be marked as read-only. Otherwise, the system throws UnsatisfiedLinkError.</li>
  <li>Enable CT by default: <a href="https://developer.android.com/privacy-and-security/security-config#CertificateTransparencySummary">Certificate transparency (CT)</a> is enabled by default. (On Android 16, CT is available but apps had to <a href="https://developer.android.com/privacy-and-security/security-config#certificateTransparency">opt in</a>.)</li>
  <li>Local network protections: Apps targeting SDK 37 or higher have <a href="https://developer.android.com/privacy-and-security/local-network-permission#android-17-enforcement">local network access blocked by default</a>. Switch to using privacy preserving pickers if possible, and use the new <a href="https://developer.android.com/reference/kotlin/android/Manifest.permission#access_local_network"><b><code>ACCESS_LOCAL_NETWORK</code></b>permission for broad, persistent access.</li>
  <li>Background audio hardening: Starting in Android 17, the audio framework enforces <a href="https://developer.android.com/about/versions/17/changes/bg-audio">restrictions on background audio interactions</a> including audio playback, <a href="https://developer.android.com/media/optimize/audio-focus">audio focus</a> requests, and <a href="https://developer.android.com/reference/android/media/AudioManager#adjustStreamVolume(int,%20int,%20int)">volume change</a> APIs. Based on your feedback, we’ve made some changes since beta 2, including targetSDK gating while-in-use FGS enforcement and exempting alarm audio. Full details available in the <a href="https://developer.android.com/about/versions/17/changes/bg-audio">updated guidance</a>.</li>
  <li>NPU access declaration: Apps targeting Android 17 that need to directly access the NPU must declare&nbsp;<a href="https://developer.android.com/reference/kotlin/android/content/pm/PackageManager#feature_neural_processing_unit">FEATURE_NEURAL_PROCESSING_UNIT</a> in their manifest to avoid being blocked from accessing the NPU. This includes apps that use the <a href="https://ai.google.dev/edge/litert/next/npu">LiteRT NPU delegate</a>, vendor-specific SDKs, as well as the deprecated <a href="https://developer.android.com/ndk/guides/neuralnetworks">NNAPI</a>.</li>
</ul>

<h3>Get started with Android 17</h3>
<p>Your Pixel device should get Android 17 shortly if you haven't already been on the Android Beta. If you don’t have a Pixel device, you can <a href="https://developer.android.com/about/versions/17/get#on_emulator">use the 64-bit system images with the Android Emulator</a> in Android Studio. If you are currently on Android 17 Beta 4.1 and have not yet taken an Android 17 QPR1 beta, you can opt out of the program and you will then be offered the release version of Android 17 over the air.</p>
<h3>Getting the Android 17 beta on partner devices</h3>
<p>Android 17 is available in beta on handset, tablet, and foldable form factors <a href="https://developer.android.com/about/versions/17/devices">from partners</a> including Honor, iQOO, Lenovo, OnePlus, OPPO, Realme, Sharp, vivo, and Xiaomi.</p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjy5cwRcpdR2j-1KMzQPpsxvIODRLlVkaFNQEIQoNaPQa4X4rgEna5imminlwFdcSJ3xihXdUSFouOC0-ZKyK1A53cBmoaU03au-FjfsqkPXm0tPLtOaWT_7z8tqnMmQjFOr-YIKeP3BMVq8Hmd7yH0zllW1aFMuiW6AAAcDUVL7aIyCAIZUs0d_0VMdF4/s1653/android-17-beta-partners.jpg" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="624" data-original-width="1653" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjy5cwRcpdR2j-1KMzQPpsxvIODRLlVkaFNQEIQoNaPQa4X4rgEna5imminlwFdcSJ3xihXdUSFouOC0-ZKyK1A53cBmoaU03au-FjfsqkPXm0tPLtOaWT_7z8tqnMmQjFOr-YIKeP3BMVq8Hmd7yH0zllW1aFMuiW6AAAcDUVL7aIyCAIZUs0d_0VMdF4/s16000/android-17-beta-partners.jpg" /></a></div><br /><h3><br /></h3>

<p>For the best development experience with Android 17, we recommend that you use the latest Canary build of <a href="https://developer.android.com/studio/preview">Android Studio Quail</a>. Once you’re set up, here are some of the things you should do:</p>
<p>Test your current app for compatibility, learn whether your app is <a href="https://developer.android.com/about/versions/17/behavior-changes-all">affected by changes in Android 17</a>, and install your app onto a device or <a href="https://developer.android.com/studio/run/emulator">Android Emulator</a> running Android 17 and extensively test it.</p>

<p>Thank you again to everyone who participated in our Android developer preview and beta program. We're looking forward to seeing how your apps take advantage of the updates in Android 17, and have plans to bring you updates in a fast-paced release cadence going forward.</p>
<p>For complete information on Android 17 please visit the <a href="https://developer.android.com/about/versions/17">Android 17 developer site</a>.</p><br /><br />

### What’s New in Android XR: Tooling, Engine Support, and Ecosystem Updates (Google Play)
- **Published**: 2026-06-22T12:52:22.553-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/what-is-new-android-xr.html](https://android-developers.googleblog.com/2026/06/what-is-new-android-xr.html)
- **Key Topics**: General Google Play AI policy
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhqvV2dCRWK9vrpSo1I7Ac_cwY4toddOPpsMksbhxXAj-Hq9t21P8UKshJzt7YHwnNoqJBqZznxKxTx2082zSoK24KRwOh-_7cWvog23nPER5IEZuGwPuMwfG4XSg2cXQT7yC1jeo3yBhpcHQJ_QEg6P3Li_uQ2zgI1I0BERqkoYg2p5_n6H6_H5-VSDDM/s2049/MM_AndroidXR_Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhqvV2dCRWK9vrpSo1I7Ac_cwY4toddOPpsMksbhxXAj-Hq9t21P8UKshJzt7YHwnNoqJBqZznxKxTx2082zSoK24KRwOh-_7cWvog23nPER5IEZuGwPuMwfG4XSg2cXQT7yC1jeo3yBhpcHQJ_QEg6P3Li_uQ2zgI1I0BERqkoYg2p5_n6H6_H5-VSDDM/s2049/MM_AndroidXR_Meta.png" style="display: none;" /><div><i>Posted by Stevan Silva, Group Product Manager, and Vinny DaSilva, Developer Relations Engineer, Android XR</i></div><br /><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhp8kd1bgx3ffvUcC2yZv7vN9fA0YNF8jZ-dWQlzOMsBbtAIVgAAUiEKx9Mplb2UbbKy6RW2UrJmhtY_TO9skOOw6V5_NEe-3-aOHSDSyDiLQLdOyFkluWF9VcZzXWfnLk9JY3YrMZ4QR21KGzUsbNOxFk2YSh8BUzdQi4QA38s36xxWwuj7_V4UxaZzWo/s4210/MM_AndroidXR_Blog.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1254" data-original-width="4210" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhp8kd1bgx3ffvUcC2yZv7vN9fA0YNF8jZ-dWQlzOMsBbtAIVgAAUiEKx9Mplb2UbbKy6RW2UrJmhtY_TO9skOOw6V5_NEe-3-aOHSDSyDiLQLdOyFkluWF9VcZzXWfnLk9JY3YrMZ4QR21KGzUsbNOxFk2YSh8BUzdQi4QA38s36xxWwuj7_V4UxaZzWo/s16000/MM_AndroidXR_Blog.png" /></a></div><br /><div><br /><br /><p>From augmented overlays to fully immersive environments, the Android XR ecosystem is expanding rapidly, with the Samsung Galaxy XR already available today. Alongside the latest updates from <a href="https://developer.android.com/blog/posts/updates-to-the-android-xr-sdk-introducing-developer-preview-4">Google I/O</a> and this week's Augmented World Expo (AWE), we are rolling out new tooling, broader engine support, and ecosystem resources to help you build and scale experiences for Android XR.</p>

<p>To get a quick look at what’s new, check out our video recap!</p>
<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/otzSN5pSNZk" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="otzSN5pSNZk"></iframe>
</div>


<p>Ready to dive deeper? Let’s jump into the major updates that will streamline your XR development workflow.</p>

<h2>Build, Prototype, and Iterate with Developer Preview 4</h2>

<p><a href="https://developer.android.com/blog/posts/updates-to-the-android-xr-sdk-introducing-developer-preview-4">Developer Preview 4 of the Android XR SDK</a> delivers the APIs and tools you need to design and build right from your laptop. This update includes the specific libraries required to target both immersive and augmented experiences. Check out the video below for a comprehensive breakdown of the latest in Android XR:</p><br /><div class="separator" style="clear: both; text-align: center;"><iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/1KOO2lqsdaA" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="1KOO2lqsdaA"></iframe></div><br /><p><br /></p>

<p>To test all of these interactions without needing physical hardware, you can emulate  and iterate on your code entirely within <a href="https://developer.android.com/studio/preview">Android Studio</a>. Check out our tooling deep dive to see how you can use XR emulator today:</p><div class="separator" style="clear: both; text-align: center;">
<iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/saRE0t11KJY" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="saRE0t11KJY"></iframe>

<h2 style="text-align: left;">Extending your mobile apps for intelligent eyewear</h2>

<p style="text-align: left;">Building for audio and display glasses doesn't mean starting from scratch. With the <a href="https://developer.android.com/develop/xr/jetpack-xr-sdk#jetpack-projected">Jetpack Projected library</a>, you can take your existing mobile app to create a complementary augmented experience. The new release includes a <a href="https://developer.android.com/develop/xr/jetpack-xr-sdk/glasses/check-availability">Device Availability API</a> that hooks into standard Android Lifecycle states, allowing your app to natively adapt its behavior based on whether the glasses are being worn.</p>

<p style="text-align: left;">To accelerate your development journey, use <a href="https://developer.android.com/tools/agents">Android CLI</a> and the <a href="https://github.com/android/skills">display glasses skill</a> to extend your mobile app into an augmented experience. The skill is packed with specialized knowledge of Jetpack Compose Glimmer, enabling it to build your UI using our recommended design patterns.</p>

<p style="text-align: left;">We’ve also updated <a href="https://developer.android.com/develop/xr/jetpack-xr-sdk/jetpack-compose-glimmer">Jetpack Compose Glimmer</a> to optimize text legibility on optical see-through displays and provide touchpad-optimized navigation components.</p>

<p style="text-align: left;">See how it looks in action: Developers at <a href="https://play.google.com/store/apps/details?id=com.naver.labs.translator">NAVER Papago</a> are already exploring how to seamlessly bring their mobile experience directly to display glasses.</p><div class="separator" style="clear: both; text-align: center;">
<iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/bYvAvQs3f8o" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="bYvAvQs3f8o"></iframe>


<p style="text-align: left;">To learn how to leverage these tools, watch this session on extending mobile apps for AI glasses:</p><div class="separator" style="clear: both; text-align: center;"><iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/83CF7AhozJ8" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="83CF7AhozJ8"></iframe></div>

<h3 style="text-align: left;">Building global, location-based immersive experiences</h3>

<p style="text-align: left;">For developers focused on immersive experiences, Developer Preview 4 brings modern, Kotlin-first architectural upgrades across our core perception libraries. We have also introduced an early preview of the Geospatial API for wired XR glasses. By combining <a href="https://developer.android.com/develop/xr/jetpack-xr-sdk/arcore">ARCore for Jetpack XR</a> with Google's Visual Positioning System (VPS), you can anchor digital content to high-precision real-world locations.</p>

<h3 style="text-align: left;">Leverage the Platforms You Know with Expanded Engine Support</h3>

<p style="text-align: left;">We want you to build using the ecosystems and workflows you already know best. To make it easier to bring your existing XR experiences over to Android XR, we are thrilled to introduce <a href="https://developer.android.com/blog/posts/android-xr-updates-for-unity-unreal-and-godot">official support for Unreal Engine and Godot</a> alongside our existing <a href="https://unity.com/blog/unity-android-xr-wired-glasses-support">Unity's support for wired XR glasses</a>.</p>

<p style="text-align: left;">With this expansion, we are introducing the <a href="https://developer.android.com/develop/xr/engine-hub">Android XR Engine Hub</a>, a desktop tool for Windows that shortens iteration cycles by bringing real-time testing directly into your engines viewport. Catch the full breakdown of our engine updates here:</p><div class="separator" style="clear: both; text-align: center;">
<iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/nmbBWSX8l54" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="nmbBWSX8l54"></iframe>

<h3 style="text-align: left;">Apply Today for the Android XR Developer Catalyst Program</h3>

<p style="text-align: left;">In addition to providing the platform, we want to fuel your innovation directly through ecosystem resources. The <a href="https://developer.android.com/develop/xr/engine-hub">Android XR Developer Catalyst Program</a> is designed to support developers with access to pre-release hardware, including display glasses, and wired XR glasses.</p>

<p style="text-align: left;">Accepted developers will receive resources, support forums, and launch guidance to prepare their apps for Google Play. Applications are open right now, so don't wait to <a href="https://developer.android.com/develop/xr/catalyst">submit your project ideas</a>.</p>

<h3 style="text-align: left;">Start Building!</h3>

<p style="text-align: left;">The ecosystem is growing rapidly, and the tools are ready for you to explore. Samsung Galaxy XR is available now, and you can dive in today with <a href="https://developer.android.com/blog/posts/updates-to-the-android-xr-sdk-introducing-developer-preview-4">Developer Preview 4 of the Android XR SDK</a>. If you don’t have hardware yet, check out the tools and to get started with the <a href="http://google.com/url?sa=j&amp;url=http%3A%2F%2Fgoo.gle%2Fxr-setup&amp;uct=1765473974&amp;usg=L4MkW244XAfYytuJciS39GjuDv0.&amp;opi=73833047&amp;source=chat">XR Emulator in Android Studio</a>.</p>

<p style="text-align: left;">For a complete look at all of our technical sessions, browse the full <a href="https://youtube.com/playlist?list=PLWz5rJ2EKKc-feGl0F3rXtUste_8TkvZJ&amp;si=zggz4T3eiQmH5xL2">Android XR Playlist on YouTube</a> to see what else is possible. We can’t wait to see what you build!</p></div><br /></div></div></div>

### Top 3 updates for Android developer productivity (Google Play)
- **Published**: 2026-06-09T17:19:04.176-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/android-developer-productivity-updates.html](https://android-developers.googleblog.com/2026/06/android-developer-productivity-updates.html)
- **Key Topics**: AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiVRZrq_G4uVlVKLwXHoXqLsp3SGb-2GJbHfNRNmjfSPuZ9gUrLJ8_fyNTDP-_jsJowwajpxaLPFd8047rF7B5IpSE8-gXFtwVx3x4WpEqWLX3Cm-bKo9tof1j5yTLT66FmzpEnod7EK8_3vUDNZv12uDz1lnfZ5O8iOQqxfWgH0oOYXd3CXvG4IUJuRfU/s4097/MM_Dev%20Productivity_Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiVRZrq_G4uVlVKLwXHoXqLsp3SGb-2GJbHfNRNmjfSPuZ9gUrLJ8_fyNTDP-_jsJowwajpxaLPFd8047rF7B5IpSE8-gXFtwVx3x4WpEqWLX3Cm-bKo9tof1j5yTLT66FmzpEnod7EK8_3vUDNZv12uDz1lnfZ5O8iOQqxfWgH0oOYXd3CXvG4IUJuRfU/s4097/MM_Dev%20Productivity_Meta.png" style="display: none;" /><div><i>Posted by Simona Milanovic, Developer Relations Engineer</i></div><p class="post-author"></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjux_TC0rxXOwY28_pZlUZ5rOLTSjuCXAfcGOd_auXXQ1D91clcsNSmIYs939dNNL7ymPVs1Q2PTFa_FwzBnlbcnNavO6MlwlCv9U2XPUDU-5I_HeVfeS72JoCHrkmGO3bXjXpJtJK8H7glEX6hfKn78-GynO8w9RqT-N-EE37oyA2rFxy6JukihWgndFE/s8419/MM_Dev%20Productivity_Blog.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2507" data-original-width="8419" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjux_TC0rxXOwY28_pZlUZ5rOLTSjuCXAfcGOd_auXXQ1D91clcsNSmIYs939dNNL7ymPVs1Q2PTFa_FwzBnlbcnNavO6MlwlCv9U2XPUDU-5I_HeVfeS72JoCHrkmGO3bXjXpJtJK8H7glEX6hfKn78-GynO8w9RqT-N-EE37oyA2rFxy6JukihWgndFE/s16000/MM_Dev%20Productivity_Blog.png" /></a></div><br /><i><br /></i><p></p>

<p>Every year, Google I/O brings new announcements and resources across ecosystems and products, including Android development. As development shifts toward AI and agent-assisted tooling, we’ve expanded our offerings to better support you, however you decide to build for Android.</p><div class="separator" style="clear: both; text-align: center;"><div class="separator" style="clear: both; text-align: center;">
  <div style="height: 0px; overflow: hidden; padding-bottom: 56.25%; position: relative; width: 97.2%;">
    <iframe allowfullscreen="" class="BLOG_video_class" height="266" src="https://www.youtube.com/embed/7fQhKxQGy5A" style="border: 0; height: 100%; left: 0; position: absolute; top: 0; width: 100%;" width="320" youtube-src-id="7fQhKxQGy5A"></iframe>
  </div>
</div>

<p style="text-align: left;">To help you stay up to date, here is a summary of the<b> top 3 announcements for Android Developer Productivity at I/O</b>.</p>

<h2 style="text-align: left;">1. Android CLI is now stable</h2><p style="text-align: left;"><a href="https://developer.android.com/tools/agents/android-cli" style="color: #1155cc; text-decoration: underline;">Android CLI</a> is now <strong>stable at version 1.0</strong>, with more capabilities and integrations.</p>

<p style="text-align: left;">The latest version of Android CLI introduces many new features, like programmatic version lookup and support for Journeys, and bridging capability to allow agents to <strong>integrate directly with Android Studio</strong>, via the <a href="https://developer.android.com/tools/agents/android-cli#studio-check" style="color: #1155cc; font-family: monospace; text-decoration: underline;">studio command</a>.</p>

<p style="text-align: left;">Running Android Studio alongside the agent and Android CLI enables more efficient navigation in your project, more precise output, and access to <strong>Android Studio’s unique tooling</strong>, such as performance profilers, Compose Previews, and Android Device Streaming.</p><div class="separator" style="clear: both;"><div style="text-align: left;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjsMNSFKeo81-n949Gxy89kxE4j9xTtoJXnyEYGULxkjQXjndkMpdDzO74Xr2rvtuJuEooGeZeMJPf_H1UJC4YljU-jrBswJOMgsQBPm-_CO2Z2EYntVE3osq8maf2chHJHB8WvRVvvf_14TxkpARGAOGAUsqYQ-vWZtm2iUhanT-Zz3GDD2HQrQk1Jpcg/s1948/1_agy-android-studio.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1552" data-original-width="1948" height="510" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjsMNSFKeo81-n949Gxy89kxE4j9xTtoJXnyEYGULxkjQXjndkMpdDzO74Xr2rvtuJuEooGeZeMJPf_H1UJC4YljU-jrBswJOMgsQBPm-_CO2Z2EYntVE3osq8maf2chHJHB8WvRVvvf_14TxkpARGAOGAUsqYQ-vWZtm2iUhanT-Zz3GDD2HQrQk1Jpcg/w640-h510/1_agy-android-studio.png" width="640" /></a></div><div style="text-align: center;"><i>Android CLI now integrates seamlessly with Android Studio</i></div></div>

<p style="text-align: left;">Additionally, Google Antigravity now officially supports Android development, with the <strong>Android resources bundle</strong>, which includes the Android CLI and skills.</p>

<p style="text-align: left;">You can either install the bundle during onboarding after installation, or later from the <strong>Settings &gt; Customizations &gt; Build With Google Plugins</strong> menu. This provides Antigravity with all the powerful tools and knowledge of Android CLI to enable it to perform core tasks—from creating projects to deploying your app on a new virtual device—much more easily and efficiently.</p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhg5lVac9WbZ_qdkjNLaQto2LX4c0tFD9zF3QIjtGcFXePDigzX7G8xAAQdo8YX6yt7U38-meDeTRQ1TCK-a7YUvjDk6D88ZfTNOQLI-6Xza52AugLbgEyg24kIzUR67lC9k3iX8H_gxk7JUYpHxSiHAJgQkFqN0CiXD8i5k4CE8Px308kNtVbKCYegJtI/s1948/1_agy-android-cli.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1552" data-original-width="1948" height="510" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhg5lVac9WbZ_qdkjNLaQto2LX4c0tFD9zF3QIjtGcFXePDigzX7G8xAAQdo8YX6yt7U38-meDeTRQ1TCK-a7YUvjDk6D88ZfTNOQLI-6Xza52AugLbgEyg24kIzUR67lC9k3iX8H_gxk7JUYpHxSiHAJgQkFqN0CiXD8i5k4CE8Px308kNtVbKCYegJtI/w640-h510/1_agy-android-cli.png" width="640" /></a></div><div style="text-align: center;"><i>Google Antigravity now offers the Android resources bundle</i></div>

</div><p style="text-align: left;"><span style="text-align: center;">Android CLI is now available through more package managers: like </span><code style="text-align: center;">npm</code><span style="text-align: center;"> and </span><code style="text-align: center;">homebrew</code><span style="text-align: center;">.&nbsp;</span><span style="text-align: center;">For more information, check out the </span><a href="https://android-developers.googleblog.com/2026/05/android-cli-stable-1-0-agent-development.html" style="color: #1155cc; text-align: center;">Android CLI blog post</a><span style="text-align: center;"> and </span><a href="https://developer.android.com/tools/agents/android-cli" style="color: #1155cc; text-align: center;">official documentation.</a></p><div><div class="separator" style="clear: both; text-align: center;"><h2 style="text-align: left;">2. Android skills keep growing</h2><p style="text-align: left;">To help models gain expertise for specific development patterns that follow our best practices, we are continuing to <strong>expand our repository of Android skills</strong>, available through <a href="https://developer.android.com/tools/agents/android-cli#skills-add" style="color: #1155cc; text-decoration: underline;">Android CLI</a> and <a href="https://github.com/android/skills" style="color: #1155cc; text-decoration: underline;">GitHub</a>.</p>

<p style="text-align: left;">Android skills ground LLMs in <strong>specialized workflows and domain knowledge,</strong> for the most common and more complex user journeys they might struggle with. We’ve shipped a fresh <strong>new batch of skills,</strong> with now more than 17 skills for areas such as:</p><ul style="line-height: 1.6; padding-left: 24px;"><li style="text-align: left;">Adaptive UI</li><li style="text-align: left;">Display Glasses and Jetpack Compose Glimmer for XR</li><li style="text-align: left;">Migration to CameraX</li><li style="text-align: left;">Perfetto SQL and Trace Analysis</li><li style="text-align: left;">Jetpack Compose Styles API</li><li style="text-align: left;">AppFunctions</li><li style="text-align: left;">Verified email retrieval with Android Credential Manager</li><li style="text-align: left;">Engage SDK integration</li><li style="text-align: left;">Testing setup</li><li style="text-align: left;">Wear OS Jetpack Compose Material3</li></ul><br /><div class="separator" style="clear: both; text-align: center;"><img border="0" data-original-height="405" data-original-width="720" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiOV9PePtO9nHxegfJn96Lsab3Z1fD7FEsjdQ9EQ2vzNOc9es2_S6h8twazy_ief9YVabhkOUWu7xJHr-hxINrva44O7QDpt3z96UtGXbvJYtAARj4tVWK3SPuFVr2in-MSdyCdpY5aOdqRbBjtw06-n365vZv8_Or8YCDrj6FQyoVl6xxKibEJF4Nh3io/s16000/2_android_skills_dev_keynote.gif" /><i>Android skills keep growing</i></div><div class="separator" style="clear: both; text-align: center;"><i><br /></i></div><div><div style="text-align: left;">You can browse skills and install using the Android CLI commands:</div><p></p>

<pre style="background-color: #f1f3f4; border-radius: 4px; color: #188038; font-family: monospace; line-height: 1.5; padding: 10px;"><div style="text-align: left;">android skills list</div><div style="text-align: left;">android skills add –skill=&lt;skill-name&gt;</div></pre>

<p style="text-align: left;">For more information, check out the <a href="https://developer.android.com/tools/agents/android-skills" style="color: #1155cc; text-decoration: underline;">official documentation.</a></p>

<h2 style="text-align: left;">3. Android Bench adds new models</h2><p style="text-align: left;">Earlier this year, we launched <a href="https://developer.android.com/bench" style="color: #1155cc; text-decoration: underline;">Android Bench</a> - our leaderboard for <strong>testing LLMs on real-world Android development</strong> challenges and tasks, with the goal of accelerating model improvements, so you have more helpful options for AI assistance.</p><div class="separator" style="clear: both; text-align: center;"><br /></div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjb0KK5bxvuZazJH0qRgHNv7cHl9uhVwZIZprnwGTBufcU7KXLpFJzNO4tCaCJLjh4mrZIqmTuFSMyRadcJxyTsWty65oLaKwi_8L_jAWHERsWYJ6hbZf5qVoDHJCZb-i0U40B3Xz8nRg-nvFYD8cf-nFx7PPG7ffBL-w4bS9RTQx_GOdQ7RXWjUN5RTbI/s2618/AndroidBenchLeaderboard.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1488" data-original-width="2618" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjb0KK5bxvuZazJH0qRgHNv7cHl9uhVwZIZprnwGTBufcU7KXLpFJzNO4tCaCJLjh4mrZIqmTuFSMyRadcJxyTsWty65oLaKwi_8L_jAWHERsWYJ6hbZf5qVoDHJCZb-i0U40B3Xz8nRg-nvFYD8cf-nFx7PPG7ffBL-w4bS9RTQx_GOdQ7RXWjUN5RTbI/s16000/AndroidBenchLeaderboard.png" /></a></div><div style="text-align: center;"><i>Latest results from Android Bench leaderboard</i></div>

<p style="text-align: left;">You asked us to evaluate open models. So, at I/O, we added more commonly used ones, including our local model <strong>Gemma 4</strong>, to the leaderboard. We also added the latest models including <strong>Gemini 3.5 Flash.</strong></p>

<p style="text-align: left;">We are also working on increasing the difficulty of challenges we’re giving LLMs, including creating long running tasks, to continue encouraging improvements. These tasks will be coming soon to Android Bench. Check out the <a href="https://developer.android.com/bench" style="color: #1155cc;">Android Bench leaderboard</a> to see the latest results.</p>

<h2 style="text-align: left;">Android development anywhere</h2><p style="text-align: left;">By expanding our AI-assisted Android development offerings to Antigravity, through Android CLI and Android skills, and solidifying with the pro capabilities and production grade polish of Android Studio, we’re <strong>supporting Android developers wherever they choose to build.</strong></p>

<p style="text-align: left;">Have fun bringing your ideas to life faster and easier than ever before - we’re excited to see what you build in this new era of agentic development.</p><p style="text-align: left;">Check out the full <a href="https://www.youtube.com/playlist?list=PLWz5rJ2EKKc-XnEzj1_CBClxpkGwYQeLy">Developer productivity at Google I/O 2026 YouTube playlist</a> for more information.</p></div></div></div>

### Datadog delivers millions of in-depth performance insights with ProfilingManager (Google Play)
- **Published**: 2026-06-08T09:51:11.835-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/datadog-profilingmanager-performance-insights.html](https://android-developers.googleblog.com/2026/06/datadog-profilingmanager-performance-insights.html)
- **Key Topics**: AI-generated content disclosures, User safety requirements
- **Details**: <meta content="https://blogger.googleusercontent.com/img/a/AVvXsEh92CmF7Hos-AKsEmr3k9Va10fhbed32pj4r9wxbUAlpyAIh2GV0KhvsRYzkmATQgflpHYdfAgdFkRfq1ki2G7ty5wKfzoaoyYknCOEjb6Auz7r0Zcfk0tR6VCX-3o3L9fpcs419uI5iNdBiOtno7ughGWD0SGJ5n3sfWPEB7ZJ9M_HQFDLhBQ_hv3HFQ8" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/a/AVvXsEh92CmF7Hos-AKsEmr3k9Va10fhbed32pj4r9wxbUAlpyAIh2GV0KhvsRYzkmATQgflpHYdfAgdFkRfq1ki2G7ty5wKfzoaoyYknCOEjb6Auz7r0Zcfk0tR6VCX-3o3L9fpcs419uI5iNdBiOtno7ughGWD0SGJ5n3sfWPEB7ZJ9M_HQFDLhBQ_hv3HFQ8" style="display: none;" />
<p style="margin-bottom: 20px;">Posted by Alice Yuan, Developer Relations Engineer at Google, Arti Arutiunov, Product Manager at Datadog and Nikita Ogorodnikov, Staff Software Engineer at Datadog</p><p></p><p style="margin-bottom: 20px;"></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/a/AVvXsEjICmOZHTF4gmgXj1G4r5Fp48jM_W4fN9tjxbdnesvaxjUsuwmrftmILW-CErt5cXGcZp93UGtLy8fBehhZxwZ2oxtjQLNb269jHfkNA3XBHnn9JIVZbApeatdCi9gX6ylK7-5A-DzQ3VSRi8hJCNp_8699CzeD9H0y26Tl-6DO8FIafh9UQFyrpa_C9DA" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img alt="" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/a/AVvXsEjICmOZHTF4gmgXj1G4r5Fp48jM_W4fN9tjxbdnesvaxjUsuwmrftmILW-CErt5cXGcZp93UGtLy8fBehhZxwZ2oxtjQLNb269jHfkNA3XBHnn9JIVZbApeatdCi9gX6ylK7-5A-DzQ3VSRi8hJCNp_8699CzeD9H0y26Tl-6DO8FIafh9UQFyrpa_C9DA=s16000" /></a></div><br /><br /><p></p>

<p>
  Performance regressions are notoriously hard to reproduce, making regressions a massive bottleneck for mobile developers. Although signals like ANR rates indicate what issues occur in production, pinpointing the specific line of code that resulted in the performance issue has historically necessitated exhaustive manual reproduction or speculative trial-and-error experimentation.
</p>

<p>Datadog collaborated with Google to mitigate this frustration by integrating the ProfilingManager API (available on Android 15+ devices) into its Real User Monitoring (RUM) and Continuous Profiling platforms. This integration transforms the debugging workflow, allowing developers to move beyond surface-level symptoms to being able to detect the <em>why</em> behind a performance bottleneck.
</p>

By leveraging this system-level API, Datadog now processes millions of production profiles weekly across the globe according to Datadog internal data of June 2026. It provides engineering teams with a new level of visibility into real-world performance, all while maintaining a low runtime overhead for production-scale performance monitoring.

<h3 style="text-align: left;">The impact of ProfilingManager</h3><p>
  ProfilingManager is a system service introduced in Android 15 that enables apps to programmatically collect performance data such as call stack samples, field traces and memory heap dumps directly from production environments. This capability shifts the engineering paradigm from reactive manual reproduction to proactive field analysis.</p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgWVOhdnTTwX9DT3ROPHDLHKm1aJ8Z0vo5wYsHTULe7oRBqsi2-pTblEC1ggNuVXdd5rCZv6RooG4dsdOqMM_8URLUxierH3KjujbTyVSFrqNIs01zMqb_o7uXFeYECms5s_CkX1WvAPaQeO5W9bpnvD4S4BNN0mH9qbanuTukvCg8LTozhNEhY0CQ0o0Q/s1280/AANDDM_DataDog_Quote_01.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img alt="ProfilingManager is a highly performant solution for code-level insights.  Of the solutions we evaluated, it has the lowest runtime overhead,  gives deep visibility into Java, Kotlin, and C++ traces, and opens the door to gather memory profiles and system-level traces during critical moments like ANRs and out-of-memory (OOM) errors. Yi Lu, Senior Engineer at Datadog" border="0" data-original-height="720" data-original-width="1280" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgWVOhdnTTwX9DT3ROPHDLHKm1aJ8Z0vo5wYsHTULe7oRBqsi2-pTblEC1ggNuVXdd5rCZv6RooG4dsdOqMM_8URLUxierH3KjujbTyVSFrqNIs01zMqb_o7uXFeYECms5s_CkX1WvAPaQeO5W9bpnvD4S4BNN0mH9qbanuTukvCg8LTozhNEhY0CQ0o0Q/s16000/AANDDM_DataDog_Quote_01.png" /></a></div><br /><p><br /></p>

For example, a Google communications app used field traces to investigate why its cold start times were slower on newer, more powerful hardware. By diving into the field-collected traces and comparing traces across different device types, the engineer discovered a hidden scheduling issue: a background text-to-speech service was unnecessarily being prewarmed during app startup. The traces revealed that this background process was monopolizing the device's highest-performing big CPU core, forcing the app's main thread to sleep while the prewarm occurred.

<h3 style="text-align: left;">Solving the Android code-level visibility challenge</h3><p>
  Prior to the implementation of ProfilingManager, Datadog’s Real User Monitoring (RUM) focused on high-level application health and session-level telemetry to assess the user journey. Engineering teams could monitor Android performance signals like time to initial display, ANR rates, CPU load, and frozen frames. These insights extended to granular interactions, such as network latency, touch events, and main thread hangs.&nbsp;However, while this data effectively highlighted which performance bottlenecks were surfacing in the field, it provided no clear path to identifying the root cause of these failures.</p><div><span face="&quot;Google Sans&quot;, sans-serif" style="font-size: 11pt; white-space: pre-wrap;"><br /></span></div><p></p><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/a/AVvXsEjW4Lm-zE5X2trjidQ0eh9i_Bhiwd7HnkOcMeRtA_4dABpGG0EPuer564cLFK4o3eb_N_zWmBAgpOa58eygLH5hwFF6kMg_4GFC98vRN4pd1LNZ-PG9W5wyHv-ptVcmIGo1M7FNPi9PKQ9iGsyZeVfr5jDK46HJHU-1Gsc6IZJdSvhrZVavqKiZmyYar0o" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img alt="We realized that across our profiling features, performance profiling on mobile applications remained a blind spot. Teams could see that an Android user experienced a slow screen render or an ANR, but lacked the same code-level visibility they relied on for their backend services. - Bryan Antigua, Senior Product Manager at Datadog" data-original-height="720" data-original-width="1280" src="https://blogger.googleusercontent.com/img/a/AVvXsEjW4Lm-zE5X2trjidQ0eh9i_Bhiwd7HnkOcMeRtA_4dABpGG0EPuer564cLFK4o3eb_N_zWmBAgpOa58eygLH5hwFF6kMg_4GFC98vRN4pd1LNZ-PG9W5wyHv-ptVcmIGo1M7FNPi9PKQ9iGsyZeVfr5jDK46HJHU-1Gsc6IZJdSvhrZVavqKiZmyYar0o=s16000" /></a></div><br /><br /><p></p>

<p>
  To address this, Datadog needed a profiling engine capable of capturing Android traces directly from devices in production with minimal performance impact. After evaluating alternative approaches, such as writing their own trace processor using Android Debug APIs, the team selected ProfilingManager because it is the most performant solution of the profiling options they evaluated and offloads the sampling decisions overhead to the OS.
</p>

<p>
  ProfilingManager supports a wide range of collection methods, including CPU traces, call stack sampling, memory analysis through Java heap dumps and native heap profiles. It enables developers to profile production builds, upload trace files to external storage, and review them in the Perfetto trace analyzer UI. As a SaaS provider, Datadog uploads, visualizes, and analyzes these profiles collected via its SDK, providing a unified view of application health.
</p>

By centralizing high-fidelity telemetry within a unified observability API, ProfilingManager empowers Datadog and its clients to proactively monitor, investigate, and remediate complex Android performance regressions through key technical advantages:

<ul style="line-height: 1.6; margin-bottom: 20px; padding-left: 25px;">
  <li style="margin-bottom: 10px;">
    <strong>Granular session diagnostics:</strong> ProfilingManager enhances debuggability by delivering direct OS-level trace data, overcoming the visibility and alignment challenges typical of custom logging with system services. To dive deeper, developers can download these traces from Datadog to investigate further in visualization tools like the <a href="https://ui.perfetto.dev/">Perfetto UI</a>.
  </li>
  <li style="margin-bottom: 10px;">
    <strong>Automated telemetry triggers:</strong> By leveraging native system events to initiate trace recordings at key optimization points, Datadog reduces the need to build custom collection logic. While the initial rollout focuses on the <a href="https://developer.android.com/reference/android/os/ProfilingTrigger?_gl=1*xix6h8*_up*MQ..*_ga*MTc4ODI2NDgwMy4xNzc5MzE2ODcw*_ga_6HH9YJMN9M*czE3NzkzMTY4NzAkbzEkZzAkdDE3NzkzMTY4NzAkajYwJGwwJGgyMTE1NzIyNjk1#TRIGGER_TYPE_APP_FULLY_DRAWN">APP_FULLY_DRAWN </a>signal, there are already plans to expand this observability to&nbsp;include <a href="https://developer.android.com/reference/android/os/ProfilingTrigger?_gl=1*1hl4p7n*_up*MQ..*_ga*MTc4ODI2NDgwMy4xNzc5MzE2ODcw*_ga_6HH9YJMN9M*czE3NzkzMTY4NzAkbzEkZzAkdDE3NzkzMTY4NzAkajYwJGwwJGgyMTE1NzIyNjk1#TRIGGER_TYPE_ANR">ANR</a>, <a href="https://developer.android.com/reference/android/os/ProfilingTrigger?_gl=1*8x3pd*_up*MQ..*_ga*MTc4ODI2NDgwMy4xNzc5MzE2ODcw*_ga_6HH9YJMN9M*czE3NzkzMTY4NzAkbzEkZzAkdDE3NzkzMTY4NzAkajYwJGwwJGgyMTE1NzIyNjk1#TRIGGER_TYPE_OOM">OOM</a>, and <a href="https://developer.android.com/reference/android/os/ProfilingTrigger?_gl=1*1ezx2ma*_up*MQ..*_ga*MTc4ODI2NDgwMy4xNzc5MzE2ODcw*_ga_6HH9YJMN9M*czE3NzkzMTY4NzAkbzEkZzAkdDE3NzkzMTY4NzAkajYwJGwwJGgyMTE1NzIyNjk1#TRIGGER_TYPE_COLD_START">COLD_START</a> triggers.</li>
  <li style="margin-bottom: 10px;">
    <strong>Proactive trace snapshots:</strong> By interfacing directly with the system-level Perfetto service (traced), ProfilingManager utilizes a proactive background recording model designed to capture unpredictable issues. This ensures that developers receive a precise visualization of the events leading up to a performance anomaly, offering a level of insight that exceeds what is possible through manual instrumentation.
  </li>
  <li style="margin-bottom: 10px;">
    <strong>Bottleneck detection at scale:</strong> Datadog is able to synthesize telemetry from across Datadog’s global customer base to uncover regressions that only emerge under unique hardware configurations and variable network environments.
  </li>
  <li style="margin-bottom: 10px;">
    <strong>System-enforced resource stability:</strong> The API leverages sampling trace collection to ensure performance and user experience impacts remain unnoticeable.
  </li>
  <li style="margin-bottom: 10px;">
    <strong>On-device data controls:</strong>&nbsp;ProfilingManager filters out irrelevant information from other processes on-device before the profile is delivered to the app. This minimizes file sizes and ensures that only data relevant to the app's processes is provided.</li>
</ul>

<h3 style="text-align: left;">Processing millions of weekly profiles to optimize real-world apps</h3><p></p><div class="separator" style="clear: both; text-align: left;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjr2ikpIrv_Km0RiIq-khGPFHpfA5CRYHfnLj2oRxLSuTk2x8qJFoO4UyNiwMpJphecSAVR4aWcJEB7BzvkXYjkyDggRDUYhLTBGhoj5q3b6BmwA5IcsER1_k5tffie6pteW3YNkIwI5Y6rG_Ie35Xzzq-mEnfq8iinA_cd_r5ydCxfRwajPSngrY1591k/s3464/datadog-profiling-blogpost-final.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1686" data-original-width="3464" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjr2ikpIrv_Km0RiIq-khGPFHpfA5CRYHfnLj2oRxLSuTk2x8qJFoO4UyNiwMpJphecSAVR4aWcJEB7BzvkXYjkyDggRDUYhLTBGhoj5q3b6BmwA5IcsER1_k5tffie6pteW3YNkIwI5Y6rG_Ie35Xzzq-mEnfq8iinA_cd_r5ydCxfRwajPSngrY1591k/s16000/datadog-profiling-blogpost-final.png" /></a></div><i><div style="text-align: center;"><i>An example of Datadog's time to initial display measurement with&nbsp;</i></div><div style="text-align: center;"><i>stack sampling powered by ProfilingManager</i></div></i><br />Integrating a system-level profiling API into a global monitoring SDK required solving infrastructure challenges. Because ProfilingManager generates highly detailed performance traces, the Datadog engineering team had to build a pipeline capable of parsing and analyzing these profiles on the server side at scale.&nbsp;<span id="docs-internal-guid-9c101479-7fff-1728-f32c-ee2043f27f0e"><span style="font-variant-alternates: normal; font-variant-east-asian: normal; font-variant-emoji: normal; font-variant-numeric: normal; font-variant-position: normal; vertical-align: baseline;">Beyond profile collection, Datadog also emphasizes the importance of balancing sampling frequency with collecting enough data to generate meaningful insights about your application. </span></span>Datadog relies on ProfilingManager’s built-in rate limiting as a critical stability safeguard, preventing excessive telemetry requests from overburdening user devices.<br /><br />The team has been profiling Datadog's own native Android application and a number of early adopters’ applications for months, gathering millions of profiles to ensure a fast, error-free launch experience and to refine their performance-detection algorithms.&nbsp;Today, the production integration seamlessly scales across a variety of Android devices. <p></p><h3 style="text-align: left;">Conclusion</h3><p>By integrating Android’s ProfilingManager API, Datadog successfully closed the visibility gap between backend systems and mobile client applications for their customers. By processing millions of profiles weekly with negligible device overhead, Datadog equips Android developers with the code-level insights necessary to diagnose complex performance bugs instantly, helping developers build smoother applications and improve their app’s performance signals in the Play Store. To adopt the ProfilingManager API directly into your performance observability framework, check out our <a href="https://developer.android.com/topic/performance/tracing/profiling-manager/overview">documentation</a>.</p>

<p>
  In the future, Datadog aims to make Android profiling data a first-class input for coding agents to autonomously resolve performance bottlenecks, closing the feedback loop between detection and remediation. Datadog is working toward making Android profiling broadly accessible to developers.
</p>

<p style="margin-top: 25px;">
  To get started using the Datadog real user monitoring feature powered by ProfilingManager, visit <a href="https://www.datadoghq.com/dg/real-user-monitoring/android-profiling/?utm_source=inbound&amp;utm_medium=corpsite-display&amp;utm_campaign=int-rum-ww-blog-announcement-announcement-androidprofilerblog2026" style="color: #0066cc;">Datadog Mobile Real User Monitoring</a>.</p>

### Prioritizing Memory Efficiency: Essential Steps for Android 17 (Google Play)
- **Published**: 2026-06-15T11:44:25.503-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/prioritizing-memory-efficiency-steps-for-android-17.html](https://android-developers.googleblog.com/2026/06/prioritizing-memory-efficiency-steps-for-android-17.html)
- **Key Topics**: Google Play AI policies, AI-generated content disclosures, User safety requirements
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhCIAoJpwUITPS5C3_eTksMsaslwqPk7SIEQHkwEkGv8572ccdIKcdv6kNC1BOSJPAZTgX5m3liMMv4zdK58e5dWRhUfo39uas23LuhEWf13TFnDTdw-Z5mWn4JarSnC8yCET8Sw15zSF-jQ5zwALriacGK6IjAGxNg61sFtSxzndjvqXxZtJt4qxuzd9A/s2048/Engineering-Memory-Blog-Meta-3.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhCIAoJpwUITPS5C3_eTksMsaslwqPk7SIEQHkwEkGv8572ccdIKcdv6kNC1BOSJPAZTgX5m3liMMv4zdK58e5dWRhUfo39uas23LuhEWf13TFnDTdw-Z5mWn4JarSnC8yCET8Sw15zSF-jQ5zwALriacGK6IjAGxNg61sFtSxzndjvqXxZtJt4qxuzd9A/s2048/Engineering-Memory-Blog-Meta-3.png" style="display: none;" />

<div class="separator" style="clear: both; text-align: left;">
    <em>Posted by Alice Yuan, Developer Relations Engineer, Ajesh Pai, Developer Relations Engineer, and Fung Lam, Developer Relations Engineer</em>
</div>

<div class="separator" style="clear: both; text-align: center;">
    <a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhanYZz4QpaDuwP7y_ZVGCUh6TpdQxS65pBcYr-Qkawd9YFS587tnIUPnqDROlxIXzgdz6GGxluR3LzH8ZabQPWz382FDEOEDpK3GxUFywn0A54JXFtUwDPaeI0JnFhEl-6NRrcjKeFPMLozNQv_An9OcWEUA-rmXfOhWvIKRrptdblGEZHERD0P-ynFcc/s4209/Engineering-Memory-Blog-3.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;">
        <img border="0" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhanYZz4QpaDuwP7y_ZVGCUh6TpdQxS65pBcYr-Qkawd9YFS587tnIUPnqDROlxIXzgdz6GGxluR3LzH8ZabQPWz382FDEOEDpK3GxUFywn0A54JXFtUwDPaeI0JnFhEl-6NRrcjKeFPMLozNQv_An9OcWEUA-rmXfOhWvIKRrptdblGEZHERD0P-ynFcc/s16000/Engineering-Memory-Blog-3.png" />
    </a>
</div>

<p style="text-align: left;">
    While app performance is often equated with a smooth UI and fast start times, memory serves as the silent foundation upon which these visible metrics are built. It's no secret that we're seeing a shift where device memory is more important than ever. Not only have we made strides in Android memory optimizations with Android 17, we're providing the tooling and API support to help you stay ahead of stricter memory requirements later this year.
</p>

<p style="text-align: left;">
    To ensure device stability, starting in Android 17, the system will begin enforcing app memory limits based on the device's total RAM. If an app exceeds those limits, Android will kill the process with no associated stack trace.
</p>

<div style="text-align: left;">
    Beyond these forced terminations, unoptimized memory usage inevitably degrades the user experience. When the app approaches heap memory limits, it triggers frequent garbage collection—leading to noticeable UI stutters. Furthermore, when a device runs out of available memory, the system scrambles to reclaim pages, causing CPU strain, UI latency, and battery drain. If the memory shortage is too severe, it can cause Low Memory Killer (LMK) events that abruptly terminate background processes and force apps to have slow cold starts and lose user state.
</div>

<div style="text-align: left;">
    <p style="text-align: left;">To build highly performant apps and avoid these forced terminations, we recommend that you adopt the following memory optimization strategies:</p>
    <ol style="text-align: left;">
        <li><a href="#Maximize">Maximize bytecode optimization with R8</a></li>
        <li><a href="#Optimize">Optimize image loading</a></li>
        <li><a href="#Detect">Detect and fix memory leaks with Android Studio</a></li>
        <li><a href="#Trim">Trim memory when app leaves visible state</a></li>
        <li><a href="#Advanced">Advanced memory observability with ProfilingManager</a></li>
    </ol>
</div>
<br />
<div>
    <div class="separator" style="clear: both; text-align: center;">
        <iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/fOXJR5qLq54" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="fOXJR5qLq54"></iframe>
    </div>
    <div style="text-align: center;">
        <em>A condensed version of this blog post is also available in video format, go check it out!</em>
    </div>

    <h3 style="text-align: left;">Understanding Android 17 app memory limits</h3>
    <p style="text-align: left;">App memory limits are being introduced in Android 17 to prevent "one bad actor" from destroying the multitasking experience and stability of the user’s entire device.</p>
    <p style="text-align: left;">Here is a breakdown of the reasons driving this architectural change:</p>

    <div style="text-align: left;">
        <ul style="text-align: left;">
            <li><b>Preventing cascading kills:</b> When an app becomes bloated or leaks memory while holding a privileged state (e.g. it’s running a Foreground Service), it is initially shielded from the system's Low Memory Killer (LMK). As this single app grows unchecked and hoards RAM, the LMK is forced to compensate by killing off dozens of smaller, well-behaved cached apps and background jobs to reclaim space for the memory hog.</li>
            <li><b>Preserving multitasking and user state:</b> When the system is forced to purge cached apps to accommodate a single leaking process, the multitasking experience is severely degraded. Users returning to prior cached applications encounter sluggish cold starts instead of near-instant warm resumes. This inefficiency generates more CPU strain and accelerates battery depletion. It can also destroy the user’s context in recently used apps, such as scroll positions, navigation stacks, and in-game progress.</li>
        </ul>

        <div style="text-align: left;">
            <p>To determine if your app session was impacted by these constraints in the field, you can call <a href="https://developer.android.com/reference/android/app/ApplicationExitInfo#getDescription%28%29" target="_blank">getDescription()</a> within <a href="https://developer.android.com/reference/android/app/ApplicationExitInfo" target="_blank">ApplicationExitInfo</a>. If the system applied a limit, the exit reason is reported as <a href="https://developer.android.com/reference/android/app/ApplicationExitInfo#REASON_OTHER" target="_blank">REASON_OTHER</a> and the description string will contain "MemoryLimiter:AnonSwap". You can also leverage <a href="https://developer.android.com/topic/performance/tracing/profiling-manager/trigger-based-capture" target="_blank">trigger-based profiling</a> using <a href="https://developer.android.com/about/versions/17/features#anomaly-profiling-trigger" target="_blank">TRIGGER_TYPE_ANOMALY</a> to automatically capture heap dumps when the memory limit is reached. Furthermore, Android is actively working to surface more in-field memory metrics to developers within the Google Play Console.</p>
            <p>We have also expanded our <a href="https://developer.android.com/about/versions/17/behavior-changes-all#app-memory-limits" target="_blank">memory limits documentation</a> to include local debugging commands, allowing you to simulate memory constraints in your local environment and validate your application's behavior under any memory limit enforcement.&nbsp;</p>
        </div>
    </div>
</div>

<div style="text-align: left;">
    <h3 id="Maximize" style="text-align: left;">Maximize bytecode optimization with R8</h3>
    <p style="text-align: left;">A highly effective way to reduce your app's memory footprint is to enable the R8 optimizer. By shrinking classes, methods, and fields into shorter names and stripping out unused code and resources, R8 significantly reduces your app's memory footprint by minimizing the amount of resident code required during execution.&nbsp;</p>
    <p style="text-align: left;">R8 minimizes resident code, shrinking the memory footprint and lowering LMK termination risk. This results in more frequent warm starts over slow cold starts. Additionally, streamlined bytecode reduces main-thread CPU overhead, directly cutting ANR rates for a more fluid user experience. For example, the digital bank <a href="https://developer.android.com/blog/posts/monzo-boosts-performance-metrics-by-up-to-35-with-a-simple-r8-update" target="_blank">Monzo</a> enabled full R8 optimization and saw a 35% reduction in their ANR rate, a 30% improvement in cold start rate, and a 9% reduction in overall app size.</p>
</div>

<div class="separator" style="clear: both; text-align: center;">
    <a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhB61hi7-o6RYAHNOoIg1egyi6iU3iGtLbwfOb-s6r_PadBV2LZzvYtcdD00iwcApjnqmwOssOLFSHv8MG_es8WJWaJUPaO6rMY4ZcINSBFROo_1Di3LVMvIEhPldpzQsUOxV1Z7VfPwvej2fa9a7yCNwBdGOGw2LMLtPrCST6InlqF1xHds30rS76C9no/s2500/pic1-IO26_113_TSV-monzo-casestudy.jpg" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;">
        <img border="0" data-original-height="1406" data-original-width="2500" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhB61hi7-o6RYAHNOoIg1egyi6iU3iGtLbwfOb-s6r_PadBV2LZzvYtcdD00iwcApjnqmwOssOLFSHv8MG_es8WJWaJUPaO6rMY4ZcINSBFROo_1Di3LVMvIEhPldpzQsUOxV1Z7VfPwvej2fa9a7yCNwBdGOGw2LMLtPrCST6InlqF1xHds30rS76C9no/s16000/pic1-IO26_113_TSV-monzo-casestudy.jpg" />
    </a>
</div>
<div style="text-align: center;">
    <i>The digital bank <a href="https://developer.android.com/blog/posts/monzo-boosts-performance-metrics-by-up-to-35-with-a-simple-r8-update" target="_blank">Monzo</a> enabled full R8 optimization and boosted performance metrics by up to 35%.</i>
</div>

<div>
    <p style="text-align: left;">To properly configure R8 in your <code>build.gradle</code> file:</p>
    <ul style="text-align: left;">
        <li>Set <code>isShrinkResources = true</code> and <code>isMinifyEnabled = true</code>.</li>
        <li>Use <code>proguard-android-optimize.txt</code> instead of the legacy <code>proguard-android.txt</code>, which actually prevents optimizations and is no longer supported in Android Gradle Plugin 9.</li>
        <li>Remove <code>android.enableR8.fullMode = false</code> from your <code>gradle.properties</code>.</li>
    </ul>

    <p style="text-align: left;">
        If you are using reflection in your code base, then add <a href="https://developer.android.com/topic/performance/app-optimization/keep-rules-overview#where-to-add-rules" target="_blank">Keep rules</a> to prevent R8 from optimizing those parts of the code. Make sure to scope the keep rules narrowly to get the maximum optimization.
    </p>
    <p style="text-align: left;">To get the maximum optimization, make sure to follow these best practices in your keep rule file.</p>

    <ul style="text-align: left;">
        <li>Remove global options like <code>-dontoptimize</code>, <code>-dontshrink</code>, and <code>-dontobfuscate</code> that prevent R8 from optimizing the entire codebase&nbsp;</li>
        <li>Remove keep rules that prevent optimizing Android components like Activity, Services, Views or Broadcast receivers.</li>
        <li>Refine the broad package wide keep rules to target only specific classes or methods.</li>
    </ul>

    <p style="text-align: left;">To see more best practices, view our <a href="https://developer.android.com/topic/performance/app-optimization/keep-rules-best-practices" target="_blank">keep rules documentation</a>.</p>

    <h3 style="text-align: left;">Library Developer R8 Best Practices</h3>
    <p>If you are a library developer, strictly place the rules your consumers need into your <code>consumer-rules</code> file, and keep your library's internal protection rules in your <code>proguard-rules.pro</code> file. For more information on how to optimize libraries, see <a href="https://developer.android.com/topic/performance/app-optimization/library-optimization" target="_blank">Optimization for library authors</a>.</p>

    <h3 style="text-align: left;">R8 Configuration Analyzer</h3>
    <p>To audit your R8 optimization, use the <b><a href="http://developer.android.com/r8-analyzer" target="_blank">Configuration Analyzer</a></b>. Configuration analyzer shows the current state of optimization with Obfuscation, Optimization, and Shrinking scores. With configuration analyzer, you can also understand how many classes, methods or fields are prevented from optimization by each keep rule. Refine these broad package wide keep rules to unlock the maximum optimization.</p>
    <p>Using configuration analyzer, you can also identify keep rules that are subsuming other keep rules, redundant keep rules and unused keep rules.</p>
</div>

<div class="separator" style="clear: both; text-align: center;">
    <a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEib0dTmk8w7EYsDiV0Ufd8CAnpWz36-ZDC_gCGFkS_0CGz0axCxOy3RBxuaOoUbR4kzaeFBXryfSR2rkxRsmTXNrPtuJw8n1DTiZiKDqHjv3AaEXteE9TKV3QxYtwCztvY-8a0GpBlOZhVV1p0ftgdxeiKGGnO3dLu_IOt-TB_7j-ZnbR2jSr_CNYzh-bc/s2048/pic2-r8-config-analyzer.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;">
        <img border="0" data-original-height="1156" data-original-width="2048" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEib0dTmk8w7EYsDiV0Ufd8CAnpWz36-ZDC_gCGFkS_0CGz0axCxOy3RBxuaOoUbR4kzaeFBXryfSR2rkxRsmTXNrPtuJw8n1DTiZiKDqHjv3AaEXteE9TKV3QxYtwCztvY-8a0GpBlOZhVV1p0ftgdxeiKGGnO3dLu_IOt-TB_7j-ZnbR2jSr_CNYzh-bc/s16000/pic2-r8-config-analyzer.png" />
    </a>
</div>
<div style="text-align: center;">
    <i>The Configuration Analyzer shows the current state of optimization with Obfuscation, Optimization, and Shrinking scores.</i>
</div>

<div>
    <h4 style="text-align: left;"><span style="font-size: large;">R8 Agent Skill&nbsp;</span></h4>
    <p style="text-align: left;">You can also leverage the <b><a href="https://github.com/android/skills/tree/main/performance/r8-analyzer" target="_blank">R8 Agent Skill</a></b> with Android Studio agent or other AI tools to resolve misconfigurations and refine your rules resulting in improved app performance. <i>(Insights from AI-driven skills will require technical verification)</i></p>
</div>

<h3 id="Optimize" style="text-align: left;">Optimize image loading</h3>
<div>
    <p>Bitmaps are usually the largest common objects residing in your app's memory. They represent the final stage of the image loading process where compressed files, like JPEGs or PNGs, are decoded into raw pixel data for display. This means a tiny 100KB compressed image can balloon into several megabytes of RAM because memory consumption is determined by the image's pixel dimensions and color depth. Since bitmap operations are frequently on the critical path to drawing frames, unoptimized images cause severe memory bloat and UI jank.</p>
    <p>Google recommends leveraging image loading libraries <b><a href="https://github.com/coil-kt/coil" target="_blank">Coil</a></b> for Kotlin-first projects, particularly when developing with Jetpack Compose and <b><a href="https://github.com/bumptech/glide" target="_blank">Glide</a></b> for Java-based applications.</p>

    <h4 style="text-align: left;"><span style="font-size: large;">Adopt these five best practices</span></h4>
    <ol style="text-align: left;">
        <li><b>Downsample images:</b> If you’re loading bitmaps manually, avoid loading a massive image into a tiny thumbnail view; use <a href="https://developer.android.com/topic/performance/graphics/load-bitmap" target="_blank">inSampleSize</a> to load a smaller version. Glide and Coil downsamples images by default and you can configure this downsample strategy using <a href="https://bumptech.github.io/glide/javadocs/470/com/bumptech/glide/load/resource/bitmap/DownsampleStrategy.html" target="_blank">DownsampleStrategy</a> and <a href="https://coil-kt.github.io/coil/image_loaders/" target="_blank">ImageLoader</a> respectively.</li>
        <li><b>Cropping:</b> Avoid embedding padding directly into an image file for letterboxing purposes (e.g., creating a transparent border to expand an image dimensions). Rather than baking in these borders, utilize <a href="https://developer.android.com/reference/android/graphics/drawable/InsetDrawable" target="_blank">InsetDrawable</a> or apply padding directly within the View or Composable containing the bitmap.</li>
        <li><b>Config:</b> Balance memory and quality by choosing the right pixel format. Use <code>RGB_565</code> when transparency isn't needed, which uses half the memory of the default <code>ARGB_8888</code> format. In Glide you can configure this by using <a href="https://bumptech.github.io/glide/javadocs/470/com/bumptech/glide/load/DecodeFormat.html" target="_blank">DecodeFormat</a> and in Coil you can use <a href="https://coil-kt.github.io/coil/api/coil-core/coil3.request/-image-request/" target="_blank">bitmapConfig</a> property.</li>
        <li><b>Prioritize vector drawables:</b> For basic geometric assets, leverage <a href="https://developer.android.com/reference/android/graphics/drawable/ShapeDrawable" target="_blank">ShapeDrawable</a> as a lightweight alternative to decoding rasterized bitmaps. By defining these assets once via XML, you ensure they scale seamlessly across all display densities while effectively eliminating resource-driven memory bloat.</li>
        <li><b>Reuse:</b> If your application manages Bitmaps manually then to minimize memory churn, when a bitmap is no longer required, the app should call <code>bitmap.recycle()</code> and immediately discard the Bitmap reference. If you use an image loading library like Glide or Coil, return the bitmap to the library’s managed pool. By providing an existing buffer for future memory needs, the pool effectively avoids the overhead of new allocations.</li>
    </ol>

    <p style="text-align: left;">Check out our documentation on <a href="https://developer.android.com/develop/ui/compose/graphics/images/optimization" target="_blank">Optimizing performance for images</a> to learn more.</p>

    <h4 style="text-align: left;"><span style="font-size: large;">Android Studio tooling</span></h4>
    <p style="text-align: left;">You can also eliminate redundant bitmaps using Android Studio Narwhal 4. Here is how to hunt them down in five simple steps:</p>
    <ol style="text-align: left;">
        <li>Open the <b>Profiler</b> tab in Android Studio</li>
        <li>Click <b>Heap Dump</b> (or "Analyze Memory Usage") and hit record to take a snapshot of your app’s current memory state.</li>
        <li>Scan the analysis results for the <b>yellow warning triangle</b> ⚠️, which Android Studio uses to flag duplicate bitmaps being stored multiple times. Alternatively, navigate to the profiler header, choose "Filter by:" and pick the "Duplicate Bitmaps" setting.</li>
        <li>Click on any flagged entry to open the <b>Bitmap Preview</b> pane, allowing you to see exactly which image is the repeat offender.</li>
        <li>Use that visual confirmation to track down the redundant loading logic in your code and implement a better caching strategy.</li>
    </ol>
</div>

<div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiDJ6djtozFY7DzrGB-EN8ajLVueF9MdLd4mod4jhtO8YwCzU7ObOwQ2w0Bap5A5NHJ7KVnXIRQqhW8cTdcFhMJPw5FIW1WU7D_Mwm-UC9Fsdr-MOn62xijpjKcS0NeUBnO957jmogGEISNQgeZQk3BVvUWK4BknTjLiuK2TbWCqwO3uTLkjkFhLwJre7w/s2379/pic3-IO26_113_TSV%20-dup-bitmaps-cropped.jpg" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1162" data-original-width="2379" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiDJ6djtozFY7DzrGB-EN8ajLVueF9MdLd4mod4jhtO8YwCzU7ObOwQ2w0Bap5A5NHJ7KVnXIRQqhW8cTdcFhMJPw5FIW1WU7D_Mwm-UC9Fsdr-MOn62xijpjKcS0NeUBnO957jmogGEISNQgeZQk3BVvUWK4BknTjLiuK2TbWCqwO3uTLkjkFhLwJre7w/s16000/pic3-IO26_113_TSV%20-dup-bitmaps-cropped.jpg" /></a></div><div class="separator" style="clear: both; text-align: center;"><i>Look for the yellow warning triangle ⚠️ in heap dumps when using the Android Studio Profiler.</i></div>

<h3 id="Detect" style="text-align: left;">Detect and fix memory leaks with Android Studio</h3>
<p style="text-align: left;">Memory leaks in Android occur when your code holds onto an object's reference long after its lifecycle has ended. This prevents the Garbage Collector (GC) from reclaiming that memory, eventually leading to sluggish performance or OutOfMemoryError (OOM).</p>
<p style="text-align: left;">Android Studio Panda 3 features a dedicated&nbsp;<a href="https://square.github.io/leakcanary/" target="_blank">LeakCanary</a>&nbsp;profiler task, allowing developers to analyze real-time memory leaks and map traces within the IDE.</p>
<p style="text-align: left;">The LeakCanary profiler task in Android Studio actively moves the memory leak analysis from your device to your development machine, resulting in a significant performance boost during the leak analysis phase as compared to on-device leak analysis.</p>

<div class="separator" style="clear: both; text-align: center;">
    <a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjKBixtkwy1hzwA6mikjRX_6vBJ9OQ_RCYdF94HUF8kOLYzQoQrPMLh_6h9u6EGeLzgFc8yjxg3_8zlqWIDCvKa1py5gyxDXasl8JLPDHSEgPpzPyYqzcme69rRKtfIlhMtyNRWXutGXNy-4WcefhSTBhqBgobK678fqvNqL5peOz1UD6ouunLaKPmJCw0/s2048/pic4-android-studio-leaks.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;">
        <img border="0" data-original-height="975" data-original-width="2048" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjKBixtkwy1hzwA6mikjRX_6vBJ9OQ_RCYdF94HUF8kOLYzQoQrPMLh_6h9u6EGeLzgFc8yjxg3_8zlqWIDCvKa1py5gyxDXasl8JLPDHSEgPpzPyYqzcme69rRKtfIlhMtyNRWXutGXNy-4WcefhSTBhqBgobK678fqvNqL5peOz1UD6ouunLaKPmJCw0/s16000/pic4-android-studio-leaks.png" />
    </a>
</div>
<div style="text-align: center;">
    <i>LeakCanary memory leak analysis contextualized with <b>Go to declaration</b> for debugging</i>
</div>

<p style="text-align: left;">Additionally, the leak analysis is now contextualized within the IDE and fully integrated with your source code, providing features like go to declaration and other helpful code connections that drastically reduce the friction and time required to investigate and fix memory leaks.</p>

<div>
    <h4 style="text-align: left;"><span style="font-size: large;">Examples of common memory leaks&nbsp;</span></h4>
    <p style="text-align: left;">Memory leaks occur when an object persists in memory beyond its intended lifespan. This typically happens due to:</p>
    <ul style="text-align: left;">
        <li>Retaining references to Fragments, Activities, or Views that are no longer in use.</li>
        <li>Mismanaging Context references.</li>
        <li>Failing to properly unregister observers, listeners, and receivers.</li>
        <li>Creating static references to objects that are bound to components with shorter lifecycles.</li>
    </ul>

    <p style="text-align: left;">Here are a few example scenarios:</p>

    <div align="left" dir="ltr" style="margin-left: 0pt;">
        <table style="border-collapse: collapse; border-color: currentcolor; border-image: initial; border-style: none; border-width: medium; border: none; max-width: 100%; table-layout: auto; width: auto;">
            <colgroup>
                <col style="width: 15%;"></col>
                <col style="width: 42.5%;"></col>
                <col style="width: 42.5%;"></col>
            </colgroup>
            <tbody>
                <tr style="height: auto;">
                    <td style="background-color: #efefef; border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Scenario</span></p>
                    </td>
                    <td style="background-color: #efefef; border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Compose-based example</span></p>
                    </td>
                    <td style="background-color: #efefef; border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">View-based example</span></p>
                    </td>
                </tr>
                <tr style="height: auto;">
                    <td style="border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: 400;">Leaking Context</span></p>
                    </td>
                    <td style="border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin-bottom: 6pt;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Example:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Passing LocalContext.current to a ViewModel</span></p>
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Fix:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Keep <code style="font-family: &quot;Roboto Mono&quot;, monospace;">Context</code> dependent logic within the UI layer. For non-UI layers, refactor to use <a href="https://developer.android.com/training/dependency-injection" style="color: #1155cc; text-decoration: underline;">dependency injection</a> or observe UI state using <a href="https://developer.android.com/kotlin/flow" style="color: #1155cc; text-decoration: underline;">Kotlin flow</a>.</span></p>
                    </td>
                    <td style="border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin-bottom: 6pt;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Example:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Storing an <code style="font-family: &quot;Roboto Mono&quot;, monospace;">Activity</code> in a companion object or static variable.</span></p>
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Fix:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Don’t hold static references to UI components. Refactor to use <a href="https://developer.android.com/training/dependency-injection" style="color: #1155cc; text-decoration: underline;">dependency injection</a> or observe UI state using <a href="https://developer.android.com/kotlin/flow" style="color: #1155cc; text-decoration: underline;">Kotlin flow</a>.</span></p>
                    </td>
                </tr>
                <tr style="height: auto;">
                    <td style="border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: 400;">Leaking Listeners</span></p>
                    </td>
                    <td style="border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin-bottom: 6pt;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Example:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Using <code style="font-family: &quot;Roboto Mono&quot;, monospace;">DisposableEffect</code> to start a listener but leaving <code style="font-family: &quot;Roboto Mono&quot;, monospace;">onDispose</code> empty.</span></p>
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Fix:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Perform the unregistration and <a href="https://developer.android.com/develop/ui/compose/side-effects#disposableeffect" style="color: #1155cc; text-decoration: underline;">cleanup logic</a> inside the <code style="font-family: &quot;Roboto Mono&quot;, monospace;">onDispose</code> block.</span></p>
                    </td>
                    <td style="border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin-bottom: 6pt;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Example:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Registering for SensorManager updates and forgetting to unregister.</span></p>
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Fix:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Manually call <code style="font-family: &quot;Roboto Mono&quot;, monospace;">unregisterListener()</code> in <code style="font-family: &quot;Roboto Mono&quot;, monospace;">onStop()</code> or <code style="font-family: &quot;Roboto Mono&quot;, monospace;">onDestroy()</code> lifecycle.</span></p>
                    </td>
                </tr>
                <tr style="height: auto;">
                    <td style="border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: 400;">Leaking Views</span></p>
                    </td>
                    <td style="border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin-bottom: 6pt;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Example:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Holding a reference to a legacy <code style="font-family: &quot;Roboto Mono&quot;, monospace;">View</code> inside an <code style="font-family: &quot;Roboto Mono&quot;, monospace;">AndroidView</code> without a release strategy.</span></p>
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Fix:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Use the <code style="font-family: &quot;Roboto Mono&quot;, monospace;">release</code> block of the <code style="font-family: &quot;Roboto Mono&quot;, monospace;">AndroidView</code> composable to clean up the legacy <code style="font-family: &quot;Roboto Mono&quot;, monospace;">View</code>.</span></p>
                    </td>
                    <td style="border: 0.75pt solid rgb(31, 31, 31); padding: 8px; vertical-align: top;">
                        <p dir="ltr" style="line-height: 1.2; margin-bottom: 6pt;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Example:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Keeping a reference to a view binding object after the <code style="font-family: &quot;Roboto Mono&quot;, monospace;">Fragment</code> is destroyed.</span></p>
                        <p dir="ltr" style="line-height: 1.2; margin: 0px;"><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt; font-weight: bold;">Fix:</span><br /><span face="'Google Sans',sans-serif" style="color: black; font-size: 11pt;">Set the binding variable to <code>null</code> inside the <code style="font-family: &quot;Roboto Mono&quot;, monospace;">onDestroyView</code>() lifecycle method.</span></p>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<h3 id="Trim" style="text-align: left;">Trim memory when app leaves visible state</h3>
<p>Android can reclaim memory from your app or stop your app entirely if necessary to free up memory for critical tasks, as explained in <a href="https://developer.android.com/topic/performance/memory-overview" target="_blank">Overview of memory management</a>. Android will usually reclaim memory from your app when it’s not visible to the user, such as by discarding some of your app’s code and data pages in memory or compressing your heap allocations. When the user resumes your app and your app tries to access some memory that’s been reclaimed, the OS will swap that memory back in on demand. This swapping behavior can be slow, and cause unexpected jank or stutters in your app.</p>
<p>If you leave it to the OS to decide what memory to reclaim from your app, you may find that the OS reclaimed memory that you’ll need shortly after resuming your app. Instead, your app can voluntarily discard memory allocations that it can regenerate later, on demand and at a low cost. To do so, you can implement the <code>ComponentCallbacks2</code> interface. You can implement <code>onTrimMemory</code> in your <code>Activity</code>, <code>Fragment</code>, <code>Service</code>, or even your custom <code>Application</code> class. Using it in the <code>Application</code> class is highly effective for global cache management.</p>
<p>The provided <a href="https://developer.android.com/reference/android/content/ComponentCallbacks2#onTrimMemory(int)" target="_blank">onTrimMemory()</a> callback method notifies your app of lifecycle or memory-related events that present a good opportunity for your app to voluntarily reduce its memory usage.</p>
<p>In terms of memory lifecycle management, your implementation should focus <b>exclusively</b> on <code>TRIM_MEMORY_UI_HIDDEN</code> and <code>TRIM_MEMORY_BACKGROUND</code>. Since Android 14, the system has ceased delivering notifications for other legacy constants, which were formally deprecated in Android 15.</p>
<p><code>TRIM_MEMORY_UI_HIDDEN</code>: This signal indicates that your application's UI has transitioned out of the user's view. This provides an opportunity to release substantial memory allocations tied strictly to the interface—such as Bitmaps, video playback buffers, or complex animation resources.</p>
<p><code>TRIM_MEMORY_BACKGROUND</code>: At this level, your process is residing in the background and is now a candidate for termination to satisfy the system's global memory needs. To extend the duration your process remains in the cached state, and reduce the number of app cold starts, you should aggressively release any resources that can be easily reconstructed once the user resumes their session.</p>

<pre style="background-color: whitesmoke; border-radius: 4px; box-sizing: border-box; color: #333333; display: inline-block; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 10pt; line-height: 1.5; margin: 1em 0px; max-width: 100%; min-width: 60%; overflow-x: auto; padding: 12px;"><code>import android.content.ComponentCallbacks2
// Other import statements.

class MainActivity : AppCompatActivity(), ComponentCallbacks2 {

    /**
     * Release memory when the UI becomes hidden or when system resources become low.
     * @param level the memory-related event that is raised.
     */
    override fun onTrimMemory(level: Int) {

        if (level &gt;= ComponentCallbacks2.TRIM_MEMORY_UI_HIDDEN) {
            // Release memory related to UI elements, such as bitmap caches.
        }

        if (level &gt;= ComponentCallbacks2.TRIM_MEMORY_BACKGROUND) {
            // Release memory related to background processing, such as by
            // closing a database connection.
        }
    }
}</code></pre>

<p>Note: The <code>onTrimMemory</code> integration may depend on SDK support. For instance, certain games rely on their game engine to enable this capability. Please check out the <a href="https://developer.android.com/games/optimize/memory-allocation" target="_blank">game memory optimization documents</a>.</p>

<h3 id="Advanced" style="text-align: left;">Advanced memory observability with ProfilingManager</h3>
<p style="text-align: left;">To catch and diagnose memory issues in the field that cannot be reproduced locally, you should leverage the <b>ProfilingManager API</b>. Introduced in Android 15, this advanced observability API allows you to programmatically collect real-user Perfetto profiles.</p>
<p style="text-align: left;">For teams that lack a dedicated infrastructure to manage and host performance artifacts, Crashlytics is exploring a specialized solution to streamline this workflow. They are inviting developers to <a href="https://docs.google.com/forms/d/e/1FAIpQLSe299a_zSNDfa164z7yyqoDjS05ZDRN86bAQKajuAOFEQ4G-w/viewform" target="_blank">provide feedback</a>.</p>

<p style="text-align: left;"><b>Android 17 introduces new event-driven triggers</b>, most notably <code>TRIGGER_TYPE_OOM</code> and <code>TRIGGER_TYPE_ANOMALY</code>:</p>
<ul style="text-align: left;">
    <li>The <b>OOM trigger</b> automatically collects a Java heap dump at the exact moment an OutOfMemoryError crash occurs, providing precise allocation states. A collected OOM profile is provided the next time the app starts and registers the <code>registerForAllProfilingResults</code> callback.</li>
    <li>The <b>Anomaly trigger</b> detects severe performance issues, such as excessive binder spam or breached memory thresholds. The memory anomaly delivers a heap dump just prior to the system terminating the app.</li>
</ul>

<pre style="background-color: whitesmoke; border-radius: 4px; box-sizing: border-box; color: #333333; display: inline-block; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 10pt; line-height: 1.5; margin: 1em 0px; max-width: 100%; min-width: 60%; overflow-x: auto; padding: 12px;"><code>  val profilingManager =
applicationContext.getSystemService(ProfilingManager::class.java)
    val triggers = ArrayList<profilingtrigger>()


    triggers.add(ProfilingTrigger.Builder(
                 ProfilingTrigger.TRIGGER_TYPE_ANOMALY))
    val mainExecutor: Executor = Executors.newSingleThreadExecutor()
    val resultCallback = Consumer<profilingresult> { profilingResult -&gt;
        if (profilingResult.errorCode != ProfilingResult.ERROR_NONE) {
            // upload profile result to server for further analysis
            setupProfileUploadWorker(profilingResult.resultFilePath)
        }

    profilingManager.registerForAllProfilingResults(mainExecutor, resultCallback)
    profilingManager.addProfilingTriggers(triggers)</profilingresult></profilingtrigger></code></pre>

<p style="text-align: left;">
    Once you’ve collected the heap dump, you can download the profile from the server, or locally via adb pull and drag and drop the file into the <a href="http://ui.perfetto.dev" target="_blank">Perfetto UI</a>. To streamline your memory debugging workflow, use the <a href="https://perfetto.dev/docs/visualization/heap-dump-explorer" target="_blank">Heap Dump Explorer</a>, this is the new default view for heap dumps in Perfetto UI. This tool provides an intuitive interface for inspecting Java heap dumps, allowing you to visualize object allocation hierarchies, compute retained memory sizes, and identify the shortest path from garbage collection root. By leveraging the Heap Dump Explorer, you can rapidly pinpoint memory leaks, bloated retained objects such as excessive bitmap allocations, and analyze heap object allocations all in one place.
</p>

<div class="separator" style="clear: both; text-align: center;">
    <a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhobASfyUbXdAYD_MOjREv7RUhCwoNJ9sB4QDSImRfA0UrALJqwQ2ovgAF7YRt3f26UeZoIQa-yDxiSDO84gxv1XkQ8acf8E795-IgAe4tl8AM_7m7nSEuj7t_rhtpgM3f-76_lEh-k7Rltku79-VCuIDN_2Q9DRjJyouCKbxg4pDXHV2yey7V8WlG2jQM/s2048/pic5-perfettoheapdump-analyzer.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;">
        <img border="0" data-original-height="1039" data-original-width="2048" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhobASfyUbXdAYD_MOjREv7RUhCwoNJ9sB4QDSImRfA0UrALJqwQ2ovgAF7YRt3f26UeZoIQa-yDxiSDO84gxv1XkQ8acf8E795-IgAe4tl8AM_7m7nSEuj7t_rhtpgM3f-76_lEh-k7Rltku79-VCuIDN_2Q9DRjJyouCKbxg4pDXHV2yey7V8WlG2jQM/s16000/pic5-perfettoheapdump-analyzer.png" />
    </a>
</div>
<div style="text-align: center;">
    <i>Use the <a href="https://perfetto.dev/docs/visualization/heap-dump-explorer">Heap Dump Explorer</a>’s embedded flamegraph to visually inspect and navigate through objects with the highest heap allocations.</i>
</div>

<h3 style="text-align: left;">Conclusion</h3>
<p>Optimizing bytecode with R8, adopting image loading best practices, and resolving memory leaks are critical steps toward delivering a high-quality user experience while managing resources effectively under pressure. Adopting these proactive measures helps maintain app stability and performance, preventing unexpected terminations while safeguarding user context. To further your performance expertise, explore our revised <a href="https://developer.android.com/topic/performance/memory" target="_blank">memory guidance</a>.</p>

### Building Premium Android Experiences at Google I/O ‘26 (Google Play)
- **Published**: 2026-06-02T10:00:27.240-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/06/building-premium-android-experiences-google-io-26.html](https://android-developers.googleblog.com/2026/06/building-premium-android-experiences-google-io-26.html)
- **Key Topics**: Google Play AI policies, AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhKGsnLX5Gwc9xouq7Q32ltvbL7xW_d4jnCXtoEFr7emB2wzqlZEuXM8FXe22ZPSguMX-nOrxAPYja6AYBZWxF-lKJYxw09D3f2aMyjxsSi5jinnDBjJPOIFDyqVhuJC2SjOqKHLAmstGg1nhyphenhyphenJGYfp3m71TPL_i3xFAUm6PKp3uo5WVytjoRwTIoNmMVQ/s4097/MM_Differentiated%20Experiences_Meta.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhKGsnLX5Gwc9xouq7Q32ltvbL7xW_d4jnCXtoEFr7emB2wzqlZEuXM8FXe22ZPSguMX-nOrxAPYja6AYBZWxF-lKJYxw09D3f2aMyjxsSi5jinnDBjJPOIFDyqVhuJC2SjOqKHLAmstGg1nhyphenhyphenJGYfp3m71TPL_i3xFAUm6PKp3uo5WVytjoRwTIoNmMVQ/s4097/MM_Differentiated%20Experiences_Meta.png" style="display: none;" />

<div style="text-align: left;">
  <div class="separator" style="clear: both; text-align: left;"><em>Posted by Ataul Munim, Android Developer Relations Engineer</em></div>
</div>

<div class="separator" style="clear: both; text-align: center;">
  <a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjimB7lZHnz1Nqt-CPhoIzMWWup9qcJd2B3wzfmG2kX-4HwtnEfrSrp9J2e7aINQrh8SaPd_mP7DvY6nQiP_K2nEju5nOCwbTan-oVeZ8rmoW1R5CvErSIFXPeuIXS7LsB8TnZZee462-ygL5IbOZ2m_C3rAcXEiv08HrPjPrku0oB-T70JyXM6lmgxzmg/s4209/MM_Differentiated-Experiences_Blog%20(1).png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;">
    <img border="0" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjimB7lZHnz1Nqt-CPhoIzMWWup9qcJd2B3wzfmG2kX-4HwtnEfrSrp9J2e7aINQrh8SaPd_mP7DvY6nQiP_K2nEju5nOCwbTan-oVeZ8rmoW1R5CvErSIFXPeuIXS7LsB8TnZZee462-ygL5IbOZ2m_C3rAcXEiv08HrPjPrku0oB-T70JyXM6lmgxzmg/s16000/MM_Differentiated-Experiences_Blog%20(1).png" />
  </a>
</div>

<div class="separator" style="clear: both; text-align: left;">
  A truly differentiated Android experience is about delivering premium delight wherever your users are. At Google I/O ‘26, we showcased how the latest advancements in the Android ecosystem can help you elevate your app's quality while maximizing development efficiency.
</div>

<div style="text-align: left;">
  <p style="text-align: left;">To help you build apps that stand out, we're diving into the key tools and libraries designed to optimize your core performance, extend the surfaces of your app to other devices, and streamline how your app handles high-quality media.&nbsp;</p>
  <p style="text-align: left;">Here is a recap of the essential updates and sessions you need to know to deliver a next-level experience across form factors!</p>
</div>

<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/Wh3LWb_Phfk" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="Wh3LWb_Phfk"></iframe>
</div>

<h3 style="text-align: left;">Maximize app performance and ROI with the R8 Configuration Analyzer</h3>
<p>A premium experience is only as good as its foundation, and a performant foundation is what allows your app to scale across the Android ecosystem. This is especially true with the release of Android 17, which introduces conservative, device RAM-based app memory limits to target extreme memory leaks and outliers before they cause system-wide instability. To stay below these new system thresholds and prevent your app from being terminated, having a lean footprint is no longer optional: it’s a critical requirement.</p>
<p>This year, we’re making it easier to build highly optimized, fast apps by introducing the <a href="https://developer.android.com/topic/performance/app-optimization/r8-configuration-analyzer" target="_blank">R8 Configuration Analyzer</a> in Android Studio. R8 is your most powerful tool for improving app performance, but its effectiveness is often limited by overly broad "keep rules" that prevent the compiler from stripping away unused code. The new Configuration Analyzer provides optimization, obfuscation, and shrinking scores, allowing you to identify specific rules that are preventing the benefits of R8 optimization.</p>
<p>By optimizing their R8 configurations, developers at Monzo achieved a 30% improvement in cold starts and a 35% reduction in ANRs. Smaller, faster code isn't just about efficiency; it's about ensuring your app has the memory headroom to deliver delight on every form factor, from the phone to the car.</p>

<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/fOXJR5qLq54" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="fOXJR5qLq54"></iframe>
</div>

<h3 style="text-align: left;">Extend your reach with a unified approach to Widgets on Phones, Watches and Cars</h3>
<p>User interaction is shifting toward quick, glanceable moments—short bursts of information that keep users connected without needing to open the full app. To help you increase the reach of your app content, we are unifying the development experience across the Android ecosystem with Jetpack Glance. By using a consistent, Compose-based model, you can elevate the content most important to your users straight to the phone’s home screen, Wear Widgets (previously Tiles!), and cars with a familiar workflow.</p>
<p>In order to help users engage with your content and features, even outside your app, we are making widgets more expressive and adaptive with RemoteCompose. On Wear OS, RemoteCompose allows you to use the Compose tools you’re already comfortable with to define UI logic that renders natively on remote surfaces, ensuring that your glanceable experiences remain highly performant and responsive even on resource-constrained hardware. On mobile and cars, RemoteCompose is used as a new framework giving Widgets new expressive capabilities.</p>
<p>You can use Jetpack Glance (together with RemoteCompose on Wear) to deliver a cohesive user journey. Whether it’s viewing flight status on the car dashboard, checking a gate change on a watch, or managing a boarding pass from a phone widget, this shared approach maximizes your app’s presence while keeping your development effort focused and efficient.</p>

<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/VnjgKzAa0ws" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="VnjgKzAa0ws"></iframe>
</div>

<div>
  <h3 style="text-align: left;">Supercharge your media pipeline with a complete, production-ready toolkit</h3>
  <div>Android has become a world-class home for the entire media lifecycle, and we are simplifying the journey from the first capture to the final playback. By leveraging Jetpack CameraX and Media3, you can build professional-grade experiences that feel native across the entire ecosystem.&nbsp;</div>
  <p style="text-align: left;">It starts with high-fidelity capture using the CameraXViewfinder Composable, which ensures your preview remains perfectly scaled and responsive on any form factor, including foldables and tablets. Use this to build adaptive capture experiences like a picture-in-picture view for multi-tasking, or that take advantage of modern features like high-frame-rate or slow-motion capture with CameraX v1.5.<br /></p>
  <p style="text-align: left;">The new Media3 AI Effects library will provide a unified interface for premium features like Image &amp; Video Enhance, Magic Eraser, and Studio Sound. This allows you to focus on the creative intent while Media3 handles the heavy lifting of choosing the most efficient and reliable path for the device. Then, use the latest improvements in multi-asset editing with Media3 Transformer to composite your edited videos together!</p>
  <p>Complete the pipeline with tools designed for professional-grade export and viewing, including:</p>
  <ul style="text-align: left;">
    <li>CodecDB, which offers data-driven encoding recommendations tailored to specific chipsets, ensuring your exported videos maintain high visual quality with minimal noise or blurriness</li>
    <li>Scrubbing Mode in ExoPlayer to provide the buttery-smooth seeking experience users expect from premium media apps</li>
    <li>Enhanced Cast support with the new CastPlayer API in Media3</li>
  </ul>
  <p>By unifying these technical pillars, you can build a cohesive, high-performance media journey that delivers both delight for your users and high ROI for your development team.</p>
</div>

<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" height="450" src="https://www.youtube.com/embed/Ch1EwR18Dqc" style="border: 0; height: 450px; width: 100%;" width="100%" youtube-src-id="Ch1EwR18Dqc"></iframe>
</div>

<p>For more details, check out the <i>premium</i> Android experience <a href="https://youtube.com/playlist?list=PLWz5rJ2EKKc8lSdmWQ_fSpV9yEGRvEL6S&amp;si=H6-8-AbtEyTqSxeY" target="_blank">YouTube playlist</a>.</p>

### Top AI on Android updates for building intelligent experiences from Google I/O ‘26 (Google Play)
- **Published**: 2026-05-26T10:51:34.948-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/05/android-ai-intelligence-system.html](https://android-developers.googleblog.com/2026/05/android-ai-intelligence-system.html)
- **Key Topics**: General Google Play AI policy
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjqtr_NVZaXiVnywBK8bKIamZw4oM3DFopMeWXl_DsHJktlRpmuCkOCQEkc85z-xJ8id7DT8ggl6OopYCndxxYb8kA2LIttV3DlL1Mzmt5OffK_Lyq1q_mxg4RdUjQ23rOyNY5N3wopBtBODH-HQsPRqBc8cS8Kw0Azhz14Jn8EjEdKQ3znXGLRVUpM_-g/s4097/Blog_Meta@2x.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjqtr_NVZaXiVnywBK8bKIamZw4oM3DFopMeWXl_DsHJktlRpmuCkOCQEkc85z-xJ8id7DT8ggl6OopYCndxxYb8kA2LIttV3DlL1Mzmt5OffK_Lyq1q_mxg4RdUjQ23rOyNY5N3wopBtBODH-HQsPRqBc8cS8Kw0Azhz14Jn8EjEdKQ3znXGLRVUpM_-g/s4097/Blog_Meta@2x.png" style="display: none;" />



<i>Posted by Jingyu Shi, Staff Developer Relations Engineer</i><div><i><br /></i><div><name content="IMG" twitter:image=""><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgnWqvWK7oNvOOsTjwsLlEtnmvh7HwduYCahIBBtGUCUZQmQ0pfEWvk3hH0xlrnhyi5oZzY_ZU22jLYl-IA00DVLLi0No_oYWTXYZSk95GLU5P-IirCS74fx2MAUV5mKO_p_6SvFiiNmFnuUoet0QHyMjc8TeLE4Ie7HE3wcFfNeFzkN66IDCkNx1QYQiI/s8419/BLOG%20HERO_BLOGGER@2x.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="2507" data-original-width="8419" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgnWqvWK7oNvOOsTjwsLlEtnmvh7HwduYCahIBBtGUCUZQmQ0pfEWvk3hH0xlrnhyi5oZzY_ZU22jLYl-IA00DVLLi0No_oYWTXYZSk95GLU5P-IirCS74fx2MAUV5mKO_p_6SvFiiNmFnuUoet0QHyMjc8TeLE4Ie7HE3wcFfNeFzkN66IDCkNx1QYQiI/s16000/BLOG%20HERO_BLOGGER@2x.png" /></a></div><br /><i><br /></i><p></p><p><i></i></p><br /></name><div>At Google I/O 2026, we introduced Android’s shift from an operating system to an intelligence system. We also demonstrated how you can build intelligent experiences natively with the system and bring the power of Google’s AI into your apps. If you missed these updates, check out our quick recap video here:&nbsp;</div><div><div><name content="IMG" twitter:image=""><br /><div class="separator" style="clear: both; text-align: center;">
<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" src="https://www.youtube.com/embed/TZNu9u9TfN4" style="aspect-ratio: 16/9; border: 0; max-width: 800px; width: 100%;"  youtube-src-id="TZNu9u9TfN4">
  </iframe>
</div>
  <br /></div></name><h4 style="text-align: left;"><name content="IMG" twitter:image=""><b><span style="font-size: large;">1. Putting your apps at the center of the intelligence system</span></b></name></h4><name content="IMG" twitter:image=""><div>The Android OS already enables agents like <a href="https://www.android.com/gemini-intelligence/?utm_source=blog.google&amp;utm_medium=owned&amp;utm_campaign=next">Gemini</a> to complete task automation, where it can navigate an app on the users behalf.&nbsp;</div><div><br /></div><div><a href="https://developer.android.com/ai/appfunctions">AppFunctions</a> (Android MCP) provides you with more control over how your app integrates with the intelligence system. This new platform API and Jetpack library are currently available in experimental preview.&nbsp;</div><p></p><ul style="text-align: left;"><li><name content="IMG" twitter:image=""><b>Android MCP:</b> AppFunctions allows your application to act as an on-device Model Context Protocol (MCP) server. It means you seamlessly share your app's tools, services and data to the system and agents.</name></li></ul><p></p><p></p><ul style="text-align: left;"><li><name content="IMG" twitter:image=""><b>Streamlined Development: </b>You can leverage the new <a href="https://github.com/android/skills/tree/main/device-ai/appfunctions">skill</a> to easily generate AppFunctions within your codebase.&nbsp; </name></li></ul><p></p><p></p><ul style="text-align: left;"><li><name content="IMG" twitter:image=""><b>Exploration and Testing:</b> We’ve released a new <a href="https://github.com/android/appfunctions/releases">test agent</a> that allows you to experiment and debug your AppFunctions in a simulated agent environment.&nbsp;</name></li></ul><span id="docs-internal-guid-8eab0469-7fff-04ab-d4bc-9e7035bdd49c"><div align="center" dir="ltr" style="margin-left: 0pt;"><table style="border-collapse: collapse; border-color: currentcolor; border-image: initial; border-style: none; border-width: medium; border: none; table-layout: fixed; width: 550pt;"><colgroup><col></col></colgroup><tbody><tr style="height: 0pt;"><td style="border-bottom: solid #000000 1pt; border-color: rgb(0, 0, 0); border-left: solid #000000 1pt; border-right: solid #000000 1pt; border-style: solid; border-top: solid #000000 1pt; border-width: 1pt; overflow-wrap: break-word; overflow: hidden; padding: 5pt; vertical-align: top;"><div style="line-height: 1.38; margin-bottom: 0pt; margin-top: 0pt;"><span face="&quot;Google Sans Text&quot;, sans-serif" style="font-variant: normal; font-weight: 700; vertical-align: baseline; white-space: pre-wrap;">Early Access Program</span><span face="&quot;Google Sans Text&quot;, sans-serif" style="font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">: Want to be among the first apps to deploy app functions in production? </span><a href="https://docs.google.com/forms/d/e/1FAIpQLScEoIsgzE-LbgRrYcQMc-Lit_5VlKRA0iWw7Pvg1brIc8wXAw/viewform" style="text-decoration: none;"><span face="&quot;Google Sans Text&quot;, sans-serif" style="color: #1155cc; font-variant: normal; text-decoration-skip-ink: none; text-decoration: underline; vertical-align: baseline; white-space: pre-wrap;">Join</span></a><span face="&quot;Google Sans Text&quot;, sans-serif" style="font-variant: normal; vertical-align: baseline; white-space: pre-wrap;"> our early access program today!</span></div></td></tr></tbody></table></div></span></name></div><div><br /></div><div>To see it in action, check out the live demo showcased during the <i>What’s New</i> in Android presentation.</div><div><br /></div><div class="separator" style="clear: both; text-align: center;">
<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" src="https://www.youtube.com/embed/2K7VVAMUYPw" style="aspect-ratio: 16/9; border: 0; max-width: 800px; width: 100%;"  youtube-src-id="2K7VVAMUYPw">
  </iframe>
</div>
  <div><div style="text-align: center;"><span style="background-color: #fcff01;"><br /></span></div><h4 style="text-align: left;"><b>&nbsp;<span style="font-size: large;">2. On-Device Power with Gemini Nano 4 Preview</span></b></h4><br /><div style="text-align: left;">Last month, we launched <a href="https://android-developers.googleblog.com/2026/04/gemma-4-new-standard-for-local-agentic-intelligence.html">Gemma 4</a>, our state-of-the-art open models. You can already preview and prototype with the next generation of Gemini Nano (Nano 4) models with the <a href="https://developers.google.com/ml-kit/genai/aicore-dev-preview">AIcore developer preview</a>. To make productionizing with Gemini Nano more reliable and performant, we are adding a few new features in <b>ML Kit GenAI APIs</b>:&nbsp;</div><br /><p></p><p></p><ul style="text-align: left;"><li><b>Prototype to Production:&nbsp;</b>Transition from prototyping in the AICore Developer Preview to building production-ready apps using the ML Kit GenAI <a href="https://developers.google.com/ml-kit/genai/prompt/android/get-started">Prompt API</a> to leverage Gemini Nano 4 that’s launching in flagship devices later this year.</li></ul><p></p><p></p><p></p><ul style="text-align: left;"><li><b>Structured Output:</b> The upcoming Structured Output API will allow you to define object classes to be returned as outputs from Prompt API, ensuring reliable outputs in productionizing your intelligent features.&nbsp;</li></ul><p></p><p></p><ul style="text-align: left;"><li><b><a href="https://developers.google.com/ml-kit/genai/prompt/android/prefix-caching">Prefix Caching</a>:</b> It optimizes your on-device inference performance with the prompt API. The new Prefix caching reduces inference time by storing and reusing the intermediate LLM state of processing a shared and recurring part of the prompt.</li></ul><p></p><div style="font-weight: bold;"><b><br /></b></div><div style="text-align: left;">For highly customized or niche use cases, you can also use LiteRT-LM to <a href="https://youtu.be/boy-UjB8hpA?si=MCPddRD7eblz8ICr">bring your own</a> fine-tuned small language model to Android.</div></div><br /><div class="separator" style="clear: both; text-align: center;">
<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" src="https://www.youtube.com/embed/Z7zx_sTbFPI" style="aspect-ratio: 16/9; border: 0; max-width: 800px; width: 100%;"  youtube-src-id="Z7zx_sTbFPI">
  </iframe>
</div>
</div><div class="separator" style="clear: both; text-align: center;"><br /></div><div class="separator" style="clear: both; text-align: center;"><br /></div><b><div style="text-align: left;"><b><span style="font-size: large;">3. Hybrid Inference &amp; Agents</span></b></div></b><div><div style="text-align: left;"><br /></div><div style="text-align: left;">To help you build more advanced AI features like hybrid inference and explore building in-app agents, we’ve released new APIs, framework and guidances:</div><p></p><p></p><ul style="text-align: left;"><li><b><a href="https://android-developers.googleblog.com/2026/04/Hybrid-inference-and-new-AI-models-are-coming-to-Android.html">Firebase AI Logic Hybrid Inference</a>: </b>This new API provides the simple routing capability between on-device models and powerful cloud infrastructure. You can set explicit orchestration modes, such as <code>PREFER_ON_DEVICE</code>, <code>PREFER_CLOUD</code>, <code>ONLY_ON_DEVICE</code>, or <code>ONLY_CLOUD</code>, based on your need.</li></ul><p></p><p></p><p></p><ul style="text-align: left;"><li><b>A2UI Jetpack Compose Renderer:</b> The new A2UI library allows your agents to "speak UI". With the upcoming Jetpack Compose Renderer, you can automatically render these A2UI messages as native UI components.</li></ul><p></p><p></p><ul style="text-align: left;"><li><b><a href="https://developers.googleblog.com/adk-kotlin-android-building-ai-agents/">ADK for Android</a>:</b> The first version of ADK for Android is available for experimentation. It allows you to build multi-agent workflows across both on-device and Cloud models while managing orchestration, context handling and sessions between agents.</li></ul><div><br /></div><div style="text-align: left;">From building with on-device models, exploring hybrid inference to building agents, you can see them in action in this talk:&nbsp;</div></div><div>&nbsp;<br /><p></p><div class="separator" style="clear: both; text-align: center;">
<div class="separator" style="clear: both; text-align: center;">
  <iframe allowfullscreen="" class="BLOG_video_class" src="https://www.youtube.com/embed/_iuXykdlTkk" style="aspect-ratio: 16/9; border: 0; max-width: 800px; width: 100%;"  youtube-src-id="_iuXykdlTkk">
  </iframe>
</div>
  </div><div class="separator" style="clear: both; text-align: center;"><br /></div><div class="separator" style="clear: both; text-align: left;"><h3 style="clear: both; text-align: left;">Start Building Today</h3><div class="separator" style="clear: both;"><div class="separator" style="clear: both;"><div class="separator" style="clear: both;">Whether you are experimenting with AppFunctions to prepare for the intelligence system, or looking to bring the power of Google’s AI within your own app, we’ve got you covered. Dive deeper into the code snippets, samples and comprehensive developer guides on the Android AI <a href="https://developer.android.com/ai">hub</a>. For the full breakdown of what’s new, check out the official <b>AI on Android at Google I/O 2026</b> <a href="https://www.youtube.com/playlist?list=PLWz5rJ2EKKc-GL3584TkxUyoPfzPkB1mV">playlist</a>.</div><div class="separator" style="clear: both;"><br /></div><div class="separator" style="clear: both;">We are excited to see what you build!&nbsp;</div><div><br /></div></div><div><br /></div></div></div></div></div></div></div></div>

### 17 Things to know for Android developers at Google I/O (Google Play)
- **Published**: 2026-05-21T09:08:56.044-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/05/17-things-android-developers-google-io.html](https://android-developers.googleblog.com/2026/05/17-things-android-developers-google-io.html)
- **Key Topics**: Google Play AI policies, AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjP7OJeCTRC-RN9j39-rULmU26qB-lZoyIZjjDrq07Z7b5GsfHz3q18ftSgcWReGBgIBkp03B6BVghzWllOC38o4jckzzq-e4a8R23ISeegev98zubhGXbIzhTZaqbCTaPLJC2zkxKYvvNspcM4yXkk94f6PEQHpdyMvlpwogicTWQRn3GEksJHOTQDIG4/s2048/GoogleForDevelopers-AndroidText-StrapiMetacard-2048x1323.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjP7OJeCTRC-RN9j39-rULmU26qB-lZoyIZjjDrq07Z7b5GsfHz3q18ftSgcWReGBgIBkp03B6BVghzWllOC38o4jckzzq-e4a8R23ISeegev98zubhGXbIzhTZaqbCTaPLJC2zkxKYvvNspcM4yXkk94f6PEQHpdyMvlpwogicTWQRn3GEksJHOTQDIG4/s2048/GoogleForDevelopers-AndroidText-StrapiMetacard-2048x1323.png" style="display: none;" />


<div style="line-height: 1.6;"><div class="separator" style="clear: both;"><div class="separator" style="clear: both; text-align: left;"><div class="separator" style="clear: both; text-align: left;"><i>Posted by Matthew McCullough, VP, Product Management, Android Developer</i></div></div></div></div><div style="line-height: 1.6;"><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjVq21_VInGStxa8CNxcwiU_tpvlkPXci8aDeSb8qUqBe4teuWUN_vIqBf_W64xjTQMBYFyJkdXB-nshsp9DXXEwzUV8-Zn9feQTbuyLk8l98kAlFQqz3_LZrYaEvCukqXCZuY95tmNzrLFqXSviaTTSxflyAkpXJb88cB7mZ7g0x6fdnKzXqY8i1jmhqM/s4209/GoogleForDevelopers-AndroidText-Blogger-4209x1253.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjVq21_VInGStxa8CNxcwiU_tpvlkPXci8aDeSb8qUqBe4teuWUN_vIqBf_W64xjTQMBYFyJkdXB-nshsp9DXXEwzUV8-Zn9feQTbuyLk8l98kAlFQqz3_LZrYaEvCukqXCZuY95tmNzrLFqXSviaTTSxflyAkpXJb88cB7mZ7g0x6fdnKzXqY8i1jmhqM/s16000/GoogleForDevelopers-AndroidText-Blogger-4209x1253.png" /></a></div><div style="line-height: 1.6;"><br /></div>Today at <a href="https://io.google/2026/">Google I/O,</a> we announced the many ways we’re powering agentic workflows to increase your productivity and ensure your apps shine across the expanding Android ecosystem. Here’s a recap of 17 of our favorite announcements for Android developers; you can also <a href="https://www.youtube.com/live/KvTRMSa1w4E?si=QBAxNvihPwJCJUuS">see what was announced last week</a> in <a href="https://developer.android.com/events/show">The Android Show: I/O Edition</a>. Stay tuned over the next two days as we dive into all of the topics in more detail!<h2 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: x-large;">Build High Quality Android Apps Using Agents</span></strong></h2>

  <h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">1: Android CLI: helping you build with any agent, LLM, and tool</span></strong></h3>
  <a href="https://goo.gle/CLI_IO26">Android CLI is now stable</a>. It offers programmatic tools that allow any AI agent, including Claude Code, Codex, or Antigravity, to perform core Android tasks much more easily and efficiently. With today’s release, it also provides a bridge to tap directly into the "heavy-lifting" power of Android Studio to give you the production-ready polish needed for professional Android development. By leveraging the new android studio commands, developers can now grant their preferred agents the ability to perform semantic symbol resolution, analyze files for warnings, and even render Jetpack Compose previews. This release also enables official support for "Journeys" through new <a href="https://developer.android.com/tools/agents/android-skills">Android skills</a>, which enables agents to execute end-to-end UI tests under your direction. Watch the <a href="https://www.youtube.com/watch?v=aqmpZocmR8o&amp;list=PLOU2XLYxmsIKL_eEgkKJWDRhYUEvS9eYz&amp;index=23">developer keynote</a>, and tune into the <a href="https://io.google/2026/explore/pa-keynote-7">What’s New in Android tools talk</a> for more information.&nbsp; &nbsp;&nbsp;<p style="color: #333333; font-family: sans-serif; text-align: center;"><span style="background-color: #fcff01;"></span></p><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhXrW3yDK9uH_I8MDyVxgYbPAXfrNTJvlMkXhaZFrM1X9ob0LvQbGe_ZC6anUeO_VNd181iptI_MIuEEpX-9GZdf6ZTJCN-WHpPzDCLOeSblo8vrjliSZ0rRrHwIsERWBjbbosP-M_WvA2pva9mF5FWVygAwQbdiW3SLZgJj9TpRIruG4H-ILsvSq_b4dc/w640-h442/agy-android-cli%20(2).png" /></div><div class="separator" style="clear: both; text-align: center;"><span><i style="background-color: white;">You can now easily install Android CLI for use with Google Antigravity 2.0.</i></span></div><p></p>

  <h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">2: Build production-ready apps with ease in Google AI Studio</span></strong></h3>
  Developers and creators can now <a href="http://android-developers.googleblog.com/2026/05/build-android-apps-google-ai-studio.html">build native Android apps, simply with a prompt in Google AI Studio</a>. The apps are built with development best practices like Jetpack Compose, Kotlin, and APIs that leverage our recommended developer patterns. Google AI Studio enables developers to prototype, iterate via an embedded emulator, and deploy to physical devices without heavy local installations. Developers are then able to take those apps and share them to Android devices, as well as share them with others for testing through Google Play Console’s internal testing track. If a developer wants to prepare their app for a wider release, they’re able to take it to Android Studio for advanced debugging, testing, and UI polish. Watch the <a href="https://www.youtube.com/watch?v=aqmpZocmR8o&amp;list=PLOU2XLYxmsIKL_eEgkKJWDRhYUEvS9eYz&amp;index=23">developer keynote</a>, and tune into the <a href="https://io.google/2026/explore/pa-keynote-7">What’s New in Android tools talk</a> for more information.<br /><br /><div style="text-align: center;"><div class="separator" style="clear: both;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjdRaw1v6rolr4alo0C6AWKdFchsMEQgtOGfmk2Ramb0IoOB7smDcVU3yC7YJMkvVQuCPJ9vQW53tQjaV-5wcgOGzMtFDmb_Jbv40an1kvQdqYburXnsONvLqckKL2MWuShi3XmQEstW761oOLjujOk3FMsh3FyAiy5-Pe7xdTwFdfkWOmEnHhQfUJhtCo/w640-h544/image1.gif" /></div><i><div class="separator" style="clear: both; text-align: center;"><i>Use the embedded Android Emulator to create Android apps in Google AI Studio</i></div></i></div><h2 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">3: Accelerating AI coding assistance with Android Bench</span></strong></h2>
  <a href="http://d.android.com/bench">Android Bench</a> is our LLM leaderboard for Android development challenges. The goal is to accelerate model improvements, so you have more useful options for AI assistance. Many of you have been using open-weight models for AI assistance, so we’re now adding commonly used ones, such as Gemma 4, to the leaderboard, so you can see how LLMs that offer offline access and additional flexibility for power-users measure up. We're continuously working on increasing the difficulty of challenges we’re giving LLMs, to continue encouraging more useful improvements.&nbsp;<h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">4: Convert iOS apps to Android with the Migration Assistant in Android Studio</span></strong></h3>
  The Migration Assistant in Android Studio is designed to port apps from platforms like iOS, React Native, or web frameworks to native Android. By simply selecting an existing project, developers can have the agent intelligently map features, convert assets like storyboards and SVGs, and implement Android best practices using Jetpack Compose and our recommended Jetpack libraries. This effectively transforms what used to be weeks of manual porting into a streamlined agentic workflow that only takes hours. We shared a preview of the incoming feature in the <a href="https://www.youtube.com/watch?v=aqmpZocmR8o&amp;list=PLOU2XLYxmsIKL_eEgkKJWDRhYUEvS9eYz&amp;index=23">developer keynote</a>.&nbsp;</div><div style="line-height: 1.6;"><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjK7UKI_nzS7gOkDXYONAjCNbQ4eSqlgT8qqMT5D4qf0OjQUNtxj4Urpq-eTROMEDgrqLKGlwMm_lHA7ayG_BC1DkitQI1ZKsF5gYr-mPIxFUsz_8JPcVHFAtnHZoO2CrVjMEvJrqvBz8_WU1I0T1P2diDprR2B47PcA21oS3RLtbgrhmrpiWV-MAw9ks4/w640-h360/image9%20(1).gif" /></div><div class="separator" style="clear: both; text-align: center;"><i>A sneak peek of the Migration Assistant converting an iOS app into a native Android app</i></div>

  <h2 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: x-large;">Building AI Into Your Apps</span></strong></h2>

  <h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">5: Building Intelligent Apps with generative AI</span></strong></h3>
  Generative AI enables you to create apps that are more intelligent, personalized, and agentic than ever before. This year, we introduced the latest advancements in on-device intelligence with a preview of Gemini Nano 4 for tasks like data extraction and summarization. We also expanded cloud capabilities via Firebase AI Logic, allowing developers to leverage Gemini models with robust grounding (including URL, Maps, and web search) to build smarter, more capable assistants. Furthermore, we unveiled our hybrid inference approach and the new <a href="https://goo.gle/ADK_IO26">Agent Development Kit (ADK) for Android</a>, alongside communication protocols like AG-UI and A2UI that simplify the creation of autonomous, agentic experiences. To start integrating these powerful features, explore the <a href="https://developer.android.com/ai">developer documentation</a>, and watch the technical deep dive session where we showcase all these technologies.

  <h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">6: Experiment with AppFunctions today</span></strong></h3>
  AppFunctions is an <a href="https://developer.android.com/reference/android/app/appfunctions/package-summary">Android platform API</a> with an accompanying <a href="https://developer.android.com/jetpack/androidx/releases/appfunctions">Jetpack library</a> to simplify building Android MCP integrations. It empowers your apps to behave like on device MCP servers, contributing functions that act as tools for use by agents and assistants. AppFunctions integration with Gemini is currently in a private preview with trusted testers, and you can begin preparing your apps already. You can sign up for the <a href="http://goo.gle/eap-af">Early Access Program</a> and start experimenting using the <a href="http://d.android.com/ai/appfunctions">API guidance</a>, <a href="https://github.com/android/appfunctions">sample</a>, and <a href="https://github.com/android/skills/blob/main/device-ai/appfunctions/SKILL.md">skill</a> today.

  <h2 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: x-large;">The Future is Adaptive</span></strong></h2>

  <h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">7: Android is now Compose First; Views are now in maintenance mode.</span></strong></h3>
  Compose is our standard for UI development, and we are moving to a Compose-first approach for all future guidance and libraries. Building on five years of evolution, the latest releases deliver a more mature toolkit, from the highly customizable Styles API to refined shared element transitions and enhanced input support. These updates allow you to build beautiful, adaptive apps with less code and better performance. Learn more about what Compose-first means for Android Development in <a href="http://android-developers.googleblog.com/2026/05/android-ui-development-is-compose-first.html">our blog post</a>.&nbsp;<br /><br /></div><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgq9kh5gxOfSdY2w9ZeKdWropXpqP7rj4KtodIZA5B_j7ujQu-blrsQKKC0lI4VEsEycpLEwsZeJhHaNOY1Xe9DrIHDwVszYfQN0GQlwxz8xoVfg1oiIr9zNlUyqqdCl2M7pyHoHgVvC7omKRthmXNaO3GE5Q15XeZ1ALiugszd8qHxpWuHo2Eh79zYW4M/w640-h416/image5.png" /></div><div style="line-height: 1.6;"><div style="text-align: center;"><i>Build Android UI with Compose</i></div><h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">8: Building seamless Android experiences across devices with Jetpack Compose</span></strong></h3><div style="text-align: left;">The Android ecosystem is now <a href="https://goo.gle/AdaptiveApps_IO26">Adaptive by Default</a>, moving fluidly across phones, foldables, tablets, cars, XR, and expanding usages with <a href="https://developer.android.com/googlebook">Googlebook</a> and connected displays. With over 580 million large-screen devices, and users on multiple devices spending up to 14x more on apps, the investment in adaptive design presents a massive opportunity. <a href="https://developer.android.com/compose">Jetpack Compose</a> is the definitive engine for this transition, offering core tools like our latest <a href="http://goo.gle/nav3">Jetpack Navigation 3</a> release, new experimental <a href="https://developer.android.com/develop/ui/compose/layouts/adaptive/grid">Grid</a> and <a href="https://developer.android.com/develop/ui/compose/layouts/adaptive/flexbox">FlexBox</a> layouts, enhanced non-touch input support, and <a href="https://developer.android.com/media/camera/camerax">CameraX</a> for correct camera previews across any window size. Furthermore, new <a href="https://developer.android.com/tools/agents/android-skills">skills</a> in Android Studio make updating your existing app to adopt these adaptive patterns easier than ever.

  <img src="https://blogger.googleusercontent.com/img/a/AVvXsEi3DD3G6IUrmOwYh7bMq0uieBvGL8li2W48YnUfQfa3ZXy2kD7QvPorNfAyCSmFlBs4q0csXDqmZjhyGf8UHFE2pUNjvqxLaaJhmm6QpSBumq2YkMHI1jyiTNfh5WQhEEY9hP6vWhcbbwflygdTwYzoIdnuIqoht0S6iGKk4pVCnxL2wVXYBMBlcdeneD8" /><i>Notability’s Android debut sets a new standard for premium productivity apps. Built with Jetpack Compose, Navigation 3, and Kotlin Multiplatform, it delivers an intuitive, adaptive experience across devices.</i></div><h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">9: Create seamless experiences for Googlebook</span></strong></h3>
  Last week we announced <a href="https://developer.android.com/googlebook">Googlebook</a>, a high-performance laptop that provides a large-screen canvas for your existing apps. Building with adaptive principles today helps ensure your app will work on Googlebook. Get started by reviewing relevant <a href="https://developer.android.com/design/ui/desktop">design guidance</a> and <a href="https://developer.android.com/docs/quality-guidelines/adaptive-app-quality/experiences/desktop">developer guidelines</a> for desktop experiences. Try out the new Desktop Emulator available in the Android Studio Canary to to test your apps for this form factor today.</div><div style="line-height: 1.6;"><br /></div><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtH3cjiXICi8dNCtQTDV9PTyjt4wPQBl1xA9XGKGU6FmqLRuBm9YyH7HNQsydD6H6F2GIPw2TdUsFyeu2xMFUO2Jk36k5QXjuWNdm_VE8AQftq2w2m0RPFyYfyZjTppSOjzuOEpJMzF08t9V0YZr-xI7mu31uvcRItugwvVxPUBouSmOXt1MsqbB1WPC0/w640-h360/image3.png" /></div><div style="line-height: 1.6;"><div style="text-align: center;"><i>New Desktop Android Emulator</i></div><h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">10: Unified widget development experience with Jetpack Glance</span></strong></h3>
  Android 17 marks a shift toward a single, Compose-based development model for all widgets. By unifying the experience across mobile, Wear OS, and cars through Jetpack Glance, you can soon scale UI components across the ecosystem with a familiar workflow. <br /><br />The breakthrough this year is the integration of RemoteCompose. On mobile and cars, it powers high-fidelity animations, while on Wear OS, it allows Wear Widgets (formerly Tiles) to render complex UI logic natively on remote surfaces. This ensures peak performance on low-power hardware while allowing a cohesive user journey—like checking a flight status on your car dashboard and seeing gate change updates on your wrist.</div><div style="line-height: 1.6;"><br /></div><div style="line-height: 1.6; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiA5s4g4hCW89qdeC2oqrTtxh6q7t9q3-wkOSt3tfVzCT3vhLUd1GMYJrhCjK04O2jyxBGl0R2pclnRq3Kb0f0Td-hV9aukKvZQTfGpGJS6GLK0MqUkpVW_0qiNC1eMGe6NPPhlCHrnQWFYhmbdSzpDnUHh5tjvpmUzZOvY2w_dX1LBnpNctSRmeahXUl4/w640-h320/blog_widgets.gif" /></div><div style="line-height: 1.6; text-align: center;"><i>Four widgets are shown cycling through in the Android Auto interface. A clock, a contact card, Google Home favorites and a photo.</i></div><div style="line-height: 1.6; text-align: center;"><i><br /></i></div><div style="line-height: 1.6;"><strong style="color: #333333;"><span style="font-family: inherit; font-size: large;">11: Expand your reach on the road with Android for Cars</span></strong><br />To help you expand your reach when you build in-car experiences, we're making it easier to build once and deliver your apps to Android Auto and Android Automotive OS. With the latest releases of the Car App Library, you can build customized, distraction-optimized&nbsp;<a href="https://developer.android.com/training/cars/apps/media">templated media apps</a>&nbsp;for both platforms. We're introducing new&nbsp;<a href="https://developer.android.com/design/ui/cars/guides/components/overview">components</a>&nbsp;and template capabilities to give you increased flexibility and more options for laying out content. Parked experiences are expanding too, with immersive video playback coming to Android Auto for phones running Android 17. You can easily adapt your video apps for these parked experiences;&nbsp;<a href="https://docs.google.com/forms/d/e/1FAIpQLSf0z4Nfw8wrloVhlgHDpLgdkg4WXsFj9ni5c1pw0qTvJ3Q4fQ/viewform">apply now to the early access program</a>&nbsp;to publish in these beta categories and learn more about the latest updates in our&nbsp;<a href="http://android-developers.googleblog.com/2026/05/android-for-cars-unifying-platforms-premium-experiences.html">blog</a>.<h3 style="color: #333333;"><strong><span style="font-family: inherit; font-size: large;">12: Accelerate your development with Android XR Developer Preview 4</span></strong></h3>Inspired by the innovative experiences you’ve built for the platform, we’re continuing to mature our tools with&nbsp;<a href="https://goo.gle/XRSDK_IO26">Developer Preview 4 of the Android XR SDK</a>. A key milestone in this journey is the transition of our core libraries, XR Runtime, Jetpack SceneCore, and ARCore for Jetpack XR, moving to Beta soon to provide a more stable and performant foundation. We are also accelerating hardware access through the&nbsp;<a href="https://goo.gle/Catalyst_IO26">Android XR Developer Catalyst Program</a>, where you can apply for XREAL’s Project Aura, audio glasses, or display glasses developer kits. Watch The latest in Android XR session or&nbsp;<a href="https://goo.gle/XRSDK_IO26">read our blog</a>&nbsp;to see how these updates help you build experiences across the ecosystem.</div><div style="line-height: 1.6;"><br /><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjyjbgGH7RwGkOkQLoXeLd88Vo7cXRjHLBSRokBWkzvYQUrqqbfrTXukM1u_SuGq0-AoXRPoGABpCOF-HMad4-aoNvXjTVyNXgGpbffTlSQMbTaXJva1c2GiUBx1fhC4fCCd0XO9XFzKNzs6edNqo0RAx-p2ZNXy0l-StJh7AxhyphenhyphenrXi-lqe-jXL0n8oprs/w640-h360/Aura%20Geospatial%20Tour%20Demo%20-%20Draft%2001%20(1).gif" /></div><i><div style="text-align: center;"><i>Early preview of the Geospatial API  in ARCore for Jetpack XR, enabling high-precision anchoring of digital content to real-world locations.</i></div></i><h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">13: Android is your new home for professional-grade media experiences</span></strong></h3>
  Android 17 streamlines the entire media lifecycle with a production-ready toolkit. High-fidelity capture is now simplified with the CameraXViewfinder Composable, which handles complex scaling and responsiveness on foldables and tablets. For post-production, the new Media3 AI Effects library provides a single interface for premium features like Magic Eraser and Studio Sound, automatically optimizing for the device's hardware. <br /><br />The pipeline is completed by CodecDB, offering chipset-specific encoding recommendations to eliminate export noise, and a new Scrubbing Mode in ExoPlayer for ultra-smooth seeking. Whether you’re compositing multi-asset edits with Media3 Transformer or using the streamlined CastPlayer API, these updates ensure a professional-grade experience with significantly less development overhead.</div><div style="line-height: 1.6;"><br /><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhXXvjrWhhRUXdYJyhuu-Vnf0UP2jKcYhAvUggZJi10kndrixZdx4cD8HEhrWVmavlxAUT5N025Fx1kgOLJP5w83LDUSR3E9YzfIJUuZ3WBedFSBtI_oLgIcxSOYg-s53obwX_8HtYqfxSaz95LVzSiMAdrrwgL4T6TVETwtxxkZV2mSkkAfvYA681zNlc/w640-h542/supercharge%20(1).gif" /></div><div class="separator" style="clear: both; text-align: center;"><i>Low Light Boost and Magic Eraser in action</i></div><h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">14: Increase app discovery and engagement on Google TV</span></strong></h3>
  Pointer remotes, which enable motion-controlled input, will be a future way for users to interact with Google TV as it unlocks faster user navigation. App developers can start <a href="https://developer.android.com/training/tv/get-started/hardware#no-touchscreen">declaring support for pointing input</a> to ensure their apps are discoverable on future TVs with pointer remotes. Additionally, the Engage SDK, formerly known as the Video Discovery API, optimizes Resumption, Entitlements, and Recommendations across all Google TV form factors to boost app discovery and engagement. It’s a great time to start onboarding the Engage SDK now, since the legacy Watch Next API, which has been powering your continue watching 1.0 experience, will lose support in the 2nd half of 2027. Get all the details in our <a href="http://android-developers.googleblog.com/2026/05/increase-google-tv-app-discovery.html">blog</a>.</div><div style="line-height: 1.6;"><h3 style="color: #333333;"><strong><span style="font-family: inherit; font-size: large;">15: Performance: the foundation of a great app experience</span></strong></h3>To help developers navigate memory limits in Android 17, we've launched a suite of optimization tools. The&nbsp;<a href="https://developer.android.com/r8-analyzer">R8 Configuration Analyzer</a>&nbsp;identifies keep rules that are bloating your binary, while&nbsp;<a href="https://developer.android.com/topic/performance/tracing/profiling-manager/how-to-capture">ProfilingManager</a>&nbsp;and the integrated LeakCanary in Android Studio streamline memory leak detection. Furthermore, the new&nbsp;<a href="https://developer.android.com/android-performance-analyzer">Android Performance Analyzer</a>&nbsp;offers advanced AI integration for complex trace analysis and automated SQL query generation to pinpoint performance bottlenecks.&nbsp; &nbsp; &nbsp;<h2 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: x-large;">And The Latest on Driving Business Growth&nbsp;</span></strong></h2>

  <h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">16: What’s new in Google Play</span></strong></h3>Today's <a href="https://goo.gle/play-io26">updates from Google Play</a> help expand your reach and scale your business with less complexity. We’re redefining Play Store discovery with an immersive, short-form video format called Play Shorts, while expanding your audience beyond the store with app discovery in the Gemini app on Android and web. Plus, we’re introducing powerful new capabilities like agentic catalog management for seamless bulk price and SKU updates, and using Gemini models to enable Play Console  to pre-populate store listings from imported documents—making global localization effortless. </div><div style="line-height: 1.6;"><br /><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgOB1wGZNYGPgY0ED70X7Dtl2KiFk8kRH4fv3HrXXTWX0-xKkN4Em0mi8QAB0g2w_-4SNcTR4fJazpiQ7XI6-XKeyQniFhULKWNmV8YvyWMuQ9tosvT5ixZ0FOye27DI90R5Tra1eWX3FCX7OrWkgzhvhCD6vtfD8_6-FMfMWDvXoVv3zSTauZwraDGsM4/w640-h360/IO26_BlogInLine_App-discovery-in-Gemini_1920x1080_1605.gif" /></div><div style="text-align: center;"><i>Gemini will provide users with app suggestions during a search</i></div>

  <h3 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: large;">17: And of course, Android 17</span></strong></h3>
  Android 17 includes new performance &amp; system architecture improvements (in addition to app memory limits) like a lock-free MessageQueue and a GC with more frequent, less intensive young-generation collections to ensure system-wide stability and smoother UIs. The new <a href="https://developer.android.com/about/versions/17/features/contact-picker">contact picker</a> and <a href="https://developer.android.com/reference/android/content/Intent#ACTION_OPEN_EYE_DROPPER">eyedropper API</a> help minimize the use of sensitive permissions and unnecessary access to user data. <br /><br />Review <a href="https://developer.android.com/about/versions/17/behavior-changes-all">the behavior changes</a> to make sure your app is ready for Android 17, including <a href="https://developer.android.com/about/versions/17/behavior-changes-all#bg-audio">background audio hardening</a> and <a href="https://developer.android.com/about/versions/17/behavior-changes-all#sms-otp-all-apps">SMS OTP protection</a>. Get ready to <a href="https://developer.android.com/about/versions/17/behavior-changes-17">target Android 17</a> (API 37) with changes such as mandatory large-screen resizability, certificate transparency by default, and restricted local network access. You can start testing today by enrolling your device <a href="https://android-developers.googleblog.com/2026/04/the-fourth-beta-of-android-17.html">in the Beta</a> or using the latest 17.0 emulator images. <br /><br />One more thing. the third beta of our Android 17 quarterly platform release (QPR1) just came out, and it contains a minor SDK release to support a few features that just couldn't wait for QPR2.

  <h2 style="color: #333333; text-align: left;"><strong><span style="font-family: inherit; font-size: x-large;">Check out all of the Android &amp; Play Content at Google I/O&nbsp;</span></strong></h2>
  <p><span face="sans-serif" style="color: #333333;">This was just a preview of some of the updates for Android developers at Google I/O. Tune into <a href="https://io.google/2026/explore/pa-keynote-5">What’s New in Android</a> for the latest news and announcements and <a href="https://io.google/2026/">follow Google I/O</a> for much more over the following week!</span></p></div>

### Build native Android apps in Google AI Studio (Google Play)
- **Published**: 2026-05-19T11:08:14.540-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/05/build-android-apps-google-ai-studio.html](https://android-developers.googleblog.com/2026/05/build-android-apps-google-ai-studio.html)
- **Key Topics**: General Google Play AI policy
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjd6QUmqCnkvDT9M0IoWA6y_752MRk01nHVQOa644yYkgoMGMDk8Dy6ow6X4SqFzzODP-a1kRaNcuF-1ZyR_lk5fTfdbuEMKDvuX4s7LFaGNuMswzvMCFoYeaQ3RLf2OZPYUWN5BsnqRIsmDub85hpYZNGY7AsaHCsHlfkxLqfqm0PozMhkyqK4i6WfgGM/s2048/GoogleForDevelopers-AndroidCombo2-StrapiMetacard-2048x1323.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjd6QUmqCnkvDT9M0IoWA6y_752MRk01nHVQOa644yYkgoMGMDk8Dy6ow6X4SqFzzODP-a1kRaNcuF-1ZyR_lk5fTfdbuEMKDvuX4s7LFaGNuMswzvMCFoYeaQ3RLf2OZPYUWN5BsnqRIsmDub85hpYZNGY7AsaHCsHlfkxLqfqm0PozMhkyqK4i6WfgGM/s2048/GoogleForDevelopers-AndroidCombo2-StrapiMetacard-2048x1323.png" style="display: none;" />


<div style="line-height: 1.5;"><div class="separator" style="clear: both; text-align: left;"><i>Posted by Emma-Louise Leavey, Group Product Manager and Mike Taylor-Cai, Product Manager</i></div></div><div style="line-height: 1.5;"><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiVwPsGVUMbwR9wQP6ABNBXOWboTfwBPXTg-WwhpVo-nJsWJkXeFMUdU5lPsXYc6jh4bnFwI03EG8fIYgmwEkU8hUKHNgSfSYpDLzUgEX1kGLGoTXXfzqcIsh6ZVOHLcripkRitSymdVGwC0Hnwm1H6S-LdsKXLdkefuPp5mtBWC5H1ACTICDI_fNqsdoc/s4209/GoogleForDevelopers-AndroidCombo2-Blogger-4209x1253.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiVwPsGVUMbwR9wQP6ABNBXOWboTfwBPXTg-WwhpVo-nJsWJkXeFMUdU5lPsXYc6jh4bnFwI03EG8fIYgmwEkU8hUKHNgSfSYpDLzUgEX1kGLGoTXXfzqcIsh6ZVOHLcripkRitSymdVGwC0Hnwm1H6S-LdsKXLdkefuPp5mtBWC5H1ACTICDI_fNqsdoc/s16000/GoogleForDevelopers-AndroidCombo2-Blogger-4209x1253.png" /></a></div><br /><div style="color: black; font-family: sans-serif; font-weight: bold; padding: 10px 0px;"><br /></div>

    Starting today <a href="https://ai.dev/apps?features=build_android_app">Google AI Studio</a> can build entire Android apps for you in minutes from just a prompt. You don't need to install any software or configure any libraries, which significantly lowers the barrier to development. Whether you’re a seasoned developer looking to prototype at lightning speed or a creator building your first-ever mobile experience, you can now go from a single prompt to a high-quality, Kotlin-based Android app in AI Studio. You can easily install the app on your device, share it with others for testing, or send it to Android Studio for any further development.</div><div style="line-height: 1.5;"><h2 style="text-align: left;">The power of native Android</h2>While AI has made it easy to generate web-based apps, people want more on their mobile devices. They expect the beautiful and usable modern app design and capabilities that come with native Android user experiences, built with the Kotlin programming language using Jetpack Compose, the official and recommended toolkit for Android development. Native Android apps bring the reliability of offline support, continuous background services, and the deep integration of hardware sensors like GPS, Bluetooth, and NFC. We've brought the technology that enables you to <a href="https://developer.android.com/studio/gemini/create-a-new-project-with-ai">quickly create new projects with Gemini in Android Studio</a> directly into the web-based AI Studio. Now, you get the best of both worlds: the ease of a prompt-based interface paired with the power of the Android SDK, all in your browser, no installation required.<br /><h2 style="color: black;"><span style="font-family: inherit;">A seamless, end-to-end workflow</span></h2>
    We have streamlined the entire development lifecycle so you can focus on your idea:&nbsp;</div><div style="line-height: 1.5;"><b><br /></b></div><div style="line-height: 1.5;"><b>1. Create your app and iterate in the cloud:</b> Use the embedded Android Emulator directly in your browser to preview and interact with your app as it’s being built. No heavy SDKs to download, no local setup required.</div><div style="line-height: 1.5;"><br /><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiWOTqLBbAXBibOw5wN_-49Q21RuGxwPjhQESK5r3KctKIPz1uV4dg0_LiK0w6xxdvbLECzMHzQk-kQO9h1VdflTPKi3wM9sKrwZvLcPbtISBnL2H4acnG8gpEuPtbxpDHexKi4S8Eg_hcQv1_dZOCh78pFGi27aiWHMYZc1gsDA_Iq7SRbVRUkHhngrgw/w640-h544/AI_Studio_creation_step_v2.gif" /></div><i><div style="text-align: center;"><i>Use the embedded Android Emulator to create and edit Android Apps right in the web browser</i></div></i><div style="line-height: 1.5;"><br /></div><b>2.</b> <b>Install instantly:&nbsp;</b>Connect your Android phone using a USB cable and install your app directly from AI Studio using the integrated Android Debug Bridge (adb).</div><div style="line-height: 1.5;"><br /><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjHMqfor305bPNhs_X2ahAxG8QmtpxtLKPrq44Uh4q1OpdsZyDlAuIyKJJDk-2v75-ErSLNp8yCyHQZn-6IQ-mkz8mfedEFtEJuD6VILIhtt8ypGpXmRuqM9LoJDDNnn-xrX3_Cr2MRUUcaEhVpJgCsjrjz-kwHHQeIhq8celQjg5Rt5_S5-j-_eSYpYaU/w640-h544/AI_Studio_Install_v2.gif" /></div><div style="text-align: center;"><i>Install the app on your Android device</i></div><div style="line-height: 1.5;"><br /></div><b>3. Streamlined Publish to Google Play:&nbsp;</b>Using your <a href="https://play.google.com/console/signup">Google Play developer account</a>, you can now publish your app directly from AI Studio for testing. AI Studio will automatically create your app record, package the bundle, and upload it to an internal testing track in Google Play Developer Console. Your app is available for you to install within minutes, and you can automatically update your app on your device as you develop it further in AI Studio.&nbsp;</div><div style="line-height: 1.5;"><br /><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhqGamXSrq6MNtz-PUt17netBXi_JiOMVERsoYV2mEArG8x5f-zCbU8WwTTaClpruCTsN4o3xeyMylDJLaWe0yCteqZJghc6sEXLYwoLPbTtnoa7761JVR_XEbm2Fj20IX142L2mGzU39vuNwLVVw0bDiSwICFelQZhxO63sG9N3GCo8Xx8wHY6gPEDj8c/w640-h544/AI_Studio_Play_v3.gif" /></div><div class="separator" style="clear: both; text-align: center;"><i>Publish the app to an internal test track in Google Play</i></div>

    <br /><div style="line-height: 1.5;"><b>Seamless app development handoff&nbsp;</b></div><div style="line-height: 1.5;">As you iterate on your app in AI Studio, you may find you need more advanced Android tools or support for a wider variety of Android device types. To move beyond the browser, you can seamlessly hand off your project to <a href="https://developer.android.com/studio">Android Studio</a> by downloading a ZIP file or exporting it directly to GitHub.</div><div style="line-height: 1.5;"><br /></div><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjNTwSv8o6QwB9QYZS_OezD7WhWQZiShTEu5aJz6_oGUfOu-2RQWmANs0jgeC1G1jrsZauVbeWzLHkjoZa_Ai_cjKvgbB_-Qzqh8-obzcNf9zKTJSG4AfvXTogb0xsCxcHRS4P-LHFKk1pm8sTdDjIn8A5b9vX8GRRvHrCvN9_xoPm6hPzN1rct5Aph3Zc/w640-h206/AI_Studio_Download.png" /></div><div style="line-height: 1.5; text-align: center;"><span style="background-color: white;"><i>Download zip file of Android app project files</i></span></div><div style="line-height: 1.5; text-align: center;"><span style="background-color: white;"><i><br /></i></span></div>When transitioning to a team environment or local development, you can leverage any IDE or agent you prefer. For a specialized experience, we recommend <a href="https://developer.android.com/gemini-in-android">Gemini in Android Studio</a>, which features models designed with Android in mind, or Antigravity, which integrates <a href="https://developer.android.com/tools/agents/android-cli">Android CLI</a> commands into Google’s agentic development platform. This workflow makes building high-quality apps more accessible while giving you total flexibility in how you use AI to scale your project.</div><div style="line-height: 1.5;"><h2 style="text-align: left;">Start building today</h2><div style="line-height: 1.5;">To ensure a safe, high-quality ecosystem from day one, we have focused our initial release on specific capabilities including:</div><div style="line-height: 1.5;"><ul style="text-align: left;"><li><b>Personal utilities and simple social apps: </b>You can rapidly prototype single or multi-screen apps, such as habit trackers, study quizzes, or event itineraries.</li><li><b>Hardware-enabled experiences:</b> Because you are building native apps, you can leverage device features like the Camera, GPS/Location, Accelerometer and Bluetooth using the native Android APIs, letting you optimize hardware-level performance.</li><li><b>AI-powered experiences: </b>You can create apps that feature Gemini API integrations, seamlessly embedding powerful AI capabilities directly into your mobile experience.</li></ul></div><h2 style="color: black;"><span style="font-family: inherit;">What’s Next?</span></h2>
    <div style="line-height: 1.5;">We are moving fast to expand what’s possible for creators in AI Studio. Here is a sneak peek at what is coming soon:</div><div style="line-height: 1.5;"><ul style="text-align: left;"><li><b>Managing Google Play Test Tracks:&nbsp;</b>Coming soon, we will be adding the ability to invite testers to try your app directly from AI Studio.&nbsp;</li><li><b>Firebase integrations: </b>Out-of-the-box support for Firestore, Firebase Auth, Firebase App Check and other tooling critical for Android developers is coming soon.</li></ul></div><div style="line-height: 1.5;"><br /></div><div style="line-height: 1.5;">Head over to <a href="https://ai.dev/apps?features=build_android_app">Google AI Studio</a> right now to start building. Here is some inspiration to get you started…&nbsp;</div><div style="line-height: 1.5;"><br /></div><table border="1" style="border-collapse: collapse; color: black; font-family: sans-serif; margin-bottom: 20px; width: 100%;">
        <tbody><tr>
            <td colspan="2" style="padding: 10px;">Turn your Google Pixel Watch into an aviation assistant</td>
        </tr>
        <tr>
            <td style="padding: 10px; width: 60%;">
                <strong>Prompt:</strong><br />
                <div style="color: #555555;">Build a small airplane "6-pack" instrument app for Google Pixel Watch. The 6 instruments should include attitude indicator, airspeed indicator, altimeter, turn coordinator, vertical speed indicator, and heading indicator. Use the Google Pixel Watch's sensors to power the instruments and display them clearly. Display one instrument at a time on the display. Swiping to the left or right should cycle through the instruments.</div>
            </td>
            <td style="padding: 10px; text-align: center; width: 40%;"><div class="separator" style="clear: both;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhRi7_vRI0TgaUYUE-g6kX-Gbg5Vf8ZVNY0H5n-2p8Ml32hyphenhyphenFvWAjp5re6AWpFKHLv1-rokBy_qfXexN61uQ9bpeDE_1DKfTrY3CkepiZMkNIEC5UlvBYng_OqersnyVS5Nu_zCuJJQ2w4NBaxWDC8duVnC0ILvWEpeg49N7aoJh1z6o_-BJHfBCnZKpz0/s320/wearOS_ai_studio.gif" /></div><br /></td>
        </tr>
    </tbody></table>

    <br /><table border="1" style="border-collapse: collapse; color: black; font-family: sans-serif; margin-bottom: 20px; width: 100%;">
        <tbody><tr>
            <td colspan="2" style="padding: 10px;">Interactive Harmonium app on Google Pixel Fold</td>
        </tr>
        <tr>
            <td style="padding: 10px; width: 60%;">
                <strong>Prompt:</strong><br />
                <div style="color: #555555;">Build a Harmonium app for Pixel Fold devices, which plays like the instrument based on the hinge angle and touch gestures. The app should simulate the bellows and reeds accurately.</div>
            </td>
            <td style="padding: 10px; text-align: center; width: 40%;"><br /><div class="separator" style="clear: both;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh8hUGuJaj76omAAgO2RqZKZ_qGvgThfE0tKA-99BJ82G2UOw8h1qT5H7sM5C7n_k2tN5CD0LpJyOFor3HefsKarRPmWTo35ltnDihv2MsddEUcZN5t5fgeJWuJ60Y3XCEqqLhd7gkGyAbM6vnGau0PLE8BohPat8lQ-63fQLudrFUVRVpkFUJ9wMFX1oc/w179-h200/Tiny%20Harmonica%20demo.gif" /></div></td>
        </tr>
    </tbody></table>

    <br /><table border="1" style="border-collapse: collapse; color: black; font-family: sans-serif; margin-bottom: 20px; width: 100%;">
        <tbody><tr>
            <td colspan="2" style="padding: 10px;">An Android app for guitarists to become better musicians by jamming to backing tracks&nbsp;</td>
        </tr>
        <tr>
            <td style="padding: 10px; width: 60%;">
                <strong>Prompt:</strong><br />
                <div><div><span style="color: #555555;">Build an Android guitar practice companion app that features a two-tab navigation system: 'Fretboard' and 'Library'.</span></div><div><span style="color: #555555;"><br /></span></div><div><span style="color: #555555;">The 'Fretboard' primary screen must contain an interactive guitar neck UI that visually maps out user-selected root notes, musical scales, and chords. Above the fretboard, implement a WebView-based YouTube player configured to play embedded videos inline. Additionally, include an AI generation feature that uses Retrofit to call Gemini Lyria 3 to create custom, 30-second backing tracks based on the user's currently selected key and scale. The generated audio files and their metadata must be saved locally using a database and displayed as a list in the 'Library' tab, where users can delete or play them.</span></div><div><span style="color: #555555;"><br /></span></div><div><span style="color: #555555;">Finally, implement a persistent, globally visible mini audio player at the bottom of the screen, complete with play/pause toggles, a progress slider for seeking, and timestamp text, allowing the user to seamlessly practice on the fretboard tab while listening to their tracks.</span></div><div style="color: #555555;"><br /></div></div>
            </td>
            <td style="padding: 10px; text-align: center; width: 40%;"><br /><div class="separator" style="clear: both;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh2pWobL4G7-4deWwvMpRmtfHG1OuXyc_bHwq6fPszYT1Vztm4g_HaN28PVg6Hwd3_N2Qd82HS1QtpUGKCTUFiCuLBwMpcA-8sMC6dJtSDGKEVAaV1kxumYMZi3kTB9NnUIEf9xQPKyyfvKb8MZUyNGnYNAEHTxyHpWCEvN2xgQsj5X09LW_FHU1n0aJQg/w221-h400/guitar_app_AI_Studio.gif" /></div></td>
        </tr>
    </tbody></table>

    We are looking forward to seeing what you build next!</div><div style="line-height: 1.5;"><br /></div><div style="line-height: 1.5;">Explore this announcement and all Google I/O 2026 updates on <a href="https://io.google/2026/?utm_source=blogpost&amp;utm_medium=pr&amp;utm_campaign=devblogs&amp;utm_content=">io.google</a>.</div>

### Increasing app discovery and engagement on Google TV (Google Play)
- **Published**: 2026-05-19T11:07:58.192-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/05/increase-google-tv-app-discovery.html](https://android-developers.googleblog.com/2026/05/increase-google-tv-app-discovery.html)
- **Key Topics**: AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiQn4lINBGbNGjb1HQYUpv_Z0-JdltXyHegoQ-Ukl5l9K2ef4BSjX8c_yu0EWlnHSJnia8oXZYWvMtKxCP9t9PlJmI9GFIy34UDVfMBkEIaz3KJegu0j2TsivMZZPHg9tkIlsyK4NWd0vEq5v1MfQUay8zJ9-2QgLDLBlkqYVxnY7BaYa3QBTVRE3NKxxQ/s2048/GoogleForDevelopers-AndroidText-StrapiMetacard-2048x1323.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiQn4lINBGbNGjb1HQYUpv_Z0-JdltXyHegoQ-Ukl5l9K2ef4BSjX8c_yu0EWlnHSJnia8oXZYWvMtKxCP9t9PlJmI9GFIy34UDVfMBkEIaz3KJegu0j2TsivMZZPHg9tkIlsyK4NWd0vEq5v1MfQUay8zJ9-2QgLDLBlkqYVxnY7BaYa3QBTVRE3NKxxQ/s2048/GoogleForDevelopers-AndroidText-StrapiMetacard-2048x1323.png" style="display: none;" />


<div><div class="separator" style="clear: both; text-align: left;"><i>Posted by Paul Lammertsma, Developer Relations Engineer</i></div></div><div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjUUiNUfVyqYWETmRLzZjld7Nbk0wpVVqMlxvLssfmOzHDfOKdKI8vZkXau3HMhjkOKcXpeJ-K-JkXiKTLk9tG2XH-O5xPlj-AVfQBnelPGhzkOJwhmFeB3NqVssPj4Cnq9r1ZkAHh-44z-dq71bQOpjIz_8d1VF1m2nYs6azBGxNBrM2GOXm6uGJymbKk/s4209/GoogleForDevelopers-AndroidText-Blogger-4209x1253.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjUUiNUfVyqYWETmRLzZjld7Nbk0wpVVqMlxvLssfmOzHDfOKdKI8vZkXau3HMhjkOKcXpeJ-K-JkXiKTLk9tG2XH-O5xPlj-AVfQBnelPGhzkOJwhmFeB3NqVssPj4Cnq9r1ZkAHh-44z-dq71bQOpjIz_8d1VF1m2nYs6azBGxNBrM2GOXm6uGJymbKk/s16000/GoogleForDevelopers-AndroidText-Blogger-4209x1253.png" /></a></div><br /><i><br /></i><p dir="ltr" style="color: red; font-weight: bold; text-align: center;"><br /></p>

<p dir="ltr">
  With over 300 million monthly active devices across Google TV and Android TV, it’s clear that the living room is a massive, distinct platform for apps to accelerate growth. Today, we’re excited to share Google TV features and developer tools designed to increase the discoverability of your content and prepare your app for future TV experiences.
</p>

<h2 dir="ltr">Drive discovery and engagement with Gemini</h2>

<p dir="ltr">
  Last year, we brought our AI voice assistant, <a href="https://blog.google/products-and-platforms/platforms/google-tv/gemini-google-tv/">Gemini</a>, to our platform, so that people can easily find what to watch, learn something new on the big screen, and get everyday tasks done with just their voice.
</p>

<p dir="ltr">
  Since launch, we’ve made <a href="https://blog.google/products-and-platforms/platforms/google-tv/new-gemini-features-march-2026/">improvements</a> to how Gemini provides tailored responses to questions. Gemini shares a mix of visuals, videos, and text to help users find what they need, when they need it. For our streaming partners, Gemini is a helpful discovery engine—pulling from your app's metadata to surface your relevant content to viewers.
</p>

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhN7u9KDZ7L8CIw5cVB_qdWf6PRcm86N8RsrlWPdEYsfwchPZwFBpMaajSqkPwXXAoBP0_v0GpQsWp4_gF_SsBC0DuZlN0qVystQ3fWmHs1qU6dKclljJaea-Phak7qEoGFiu_i3-dj0l7WmA7Tm7T2v8kERsfhKp6BCFs-7y7eSdxVWmFkpIzXYsceaJM/w640-h360/GTV%20Gemini%20-%20GOAT%20overview%20%5B10.8%20MB%5D.gif" /></div>

<h2 dir="ltr">Declare support for pointing modality</h2>

<p dir="ltr">
  The TV experience that we once knew is changing. Gemini is changing the way we discover and stream content with voice, but how we use the remote is evolving, too.
</p>

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi5hNXf8y8wwFxJAgZ0N4QwO5v6QUe7vn4Qy70-ndmo2iTye1qdhKP5WxKPJVwoPi0qdadX25BUJzxtLQZVAHXASOibVD0y3Xd_gFuOzp5GOIBwtXy_2jFa4lsTi4r1k6OzkTe5HyJGkOK-fNspRoo54mEA5IB8K4f0fVZ9UpgTWlringYByYxw3Bn_X1c/w640-h360/GTV%20Pointer%20Remote%20Demo_SHELL.gif" /></div>

<p dir="ltr">
  Pointer remotes bring motion-controlled input to the big screen, unlocking faster user navigation across the Google TV Home page and within content-heavy apps. To ensure your app is ready for this shift and provides a great experience for all users, now is the time to start thinking about pointing input. Here’s how to get started:
</p>

<h4 style="text-align: left;"><span style="font-size: medium;">1. Adapt your TV app UI Library</span></h4>
<p dir="ltr">
  You’ll need support for hover states, scrollable containers, and cursor clicks to enable pointer remote interactions for your app on Google TV. While implementation varies by UI stack, Jetpack Compose streamlines this transition, as most core components handle these multi-modal interactions natively out of the box.
</p>

<ol type="a">
  <li><strong>Hover state:</strong> Every focusable element on your screen (buttons, movie posters, setting toggles) needs a clear visual feedback mechanism for a hover state. This is often subtler than a focus state but critical for feedback.</li>
  <li><strong>Scrollable containers:</strong> Pointer remotes will also have a small circular touchpad for scrolling. Users can use this touchpad to scroll up or down, or left or right in your app. Your app will need to respond to touch events to scroll.</li>
  <li><strong>Cursor clicks:</strong> Many TV apps today expect a simple D-pad OKAY button “click.” With a pointer remote, a user may “click” on an element that’s not the D-pad focus state, but is instead from a hovered state (similar to a mouse click).</li>
</ol>

<h4 style="text-align: left;"><span style="font-family: inherit; font-size: medium;">2. Test pointing interactions with a mouse today</span></h4>
<p dir="ltr">
  To see how your app handles hover, scroll, and clicks, simply connect a bluetooth mouse or wired mouse to your Google TV. Keep in mind that a mouse has more precise control, since users are closer to the screen and typically rest the mouse in a stable position. Pointer remotes can often be less precise, since users are sometimes 10 feet away from the screen, making rough gestures with the remote from their couch. As a TV designer or developer, you can mitigate this lack of input precision by having larger hover targets for elements.
</p>

<h4 style="text-align: left;"><span style="font-size: medium;">3. Declare TV app support for pointer remotes on Google Play</span></h4>
<p dir="ltr">
  Finally, tell Google Play that your TV app is designed to work with a pointer. This ensures that users with pointer remotes will be able to easily find, install, and interact with your app.
</p>

<p dir="ltr">
  Within your AndroidManifest.xml, declare the meta-data tag, <span style="color: #188038;">android.software.leanback.</span><span style="color: #9900ff; font-weight: bold;">supports_touch</span>. This tag informs the platform that your TV app “spatially supports touch,” since pointer remotes simulate touch events from a distance.
</p>

<p dir="ltr"><strong><em>AndroidManifest.xml</em></strong></p>

<pre style="background-color: #f3f3f3; border: 1pt solid rgb(217, 217, 217); overflow-x: auto; padding: 10px;">&lt;manifest ...&gt;
    &lt;!-- Signal whether the app is adaptive or built just for TV --&gt;
    &lt;uses-feature android:name="android.software.leanback" android:required="true|false" /&gt;

    &lt;!-- Ensure the app can be installed on conventional TVs --&gt;
    &lt;uses-feature android:name="android.hardware.touchscreen" android:required="false" /&gt;

    &lt;!-- Signal whether the app supports pointer remotes --&gt;
    &lt;meta-data android:name="android.software.leanback.supports_touch" android:value="true|false"/&gt;

    &lt;application ...&gt;
        ...
    &lt;/application&gt;
&lt;/manifest&gt;
</pre>

<p dir="ltr"><strong>Tips:</strong></p><ul>
  <li>The <span style="color: #188038;">android.<strong>software</strong>.<strong>leanback</strong></span> feature declaration indicates that your app supports D-pad navigation and is intended for distribution only on TV devices via Google Play.</li>
  <li>The new software attribute of <span style="color: #188038;">android.software.leanback.</span><span style="color: #9900ff; font-weight: bold;">supports_touch</span> declares that in addition to D-pad, you have ensured that your TV app works well for pointer/cursor experiences via mouse (of today) and pointer remotes (of future).</li>
  <li>If you haven't already, now is the time to adopt <a href="https://developer.android.com/compose">Jetpack Compose</a>. Hover, scroll, and clicks are common input modalities that are supported on various form factors, and building your app with an adaptive UI framework enables code reusability and reduced maintenance.</li>
</ul>

<h2 dir="ltr">Onboard the Engage SDK</h2>
<p dir="ltr">
  The Engage SDK, formerly known as the Video Discovery API, optimizes Resumption, Entitlements, and Recommendations across all Google TV form factors to boost app discovery and engagement.
</p>

<ul>
  <li><strong>Resumption:</strong> Partners can easily display a user's paused video within the 'Continue Watching' row from the Home page.</li>
  <li><strong>Entitlements:</strong> The Engage SDK streamlines entitlement management, which matches app content to user eligibility. Users appreciate this because they can enjoy personalized recommendations without needing to manually update all their subscription details. This allows partners to connect with users across multiple discovery points on Google TV.</li>
  <li><strong>Recommendations:</strong> The Engage SDK even highlights personalized recommendations based on content that users watched inside apps.</li>
</ul>

<p dir="ltr">
  It’s a great time to start onboarding the Engage SDK now, since the legacy Watch Next API, which has been powering your continue watching 1.0 experience, will lose support in the 2nd half of 2027. To get started, head to <a href="https://goo.gle/engage-tv">goo.gle/engage-tv</a> to learn more.
</p>

<p dir="ltr">
  We're excited to see how our latest Gemini experience and developer tools will optimize your discovery and drive user engagement on our platform.
</p>Explore this announcement and all Google I/O 2026 updates on <a href="https://io.google/2026/?utm_source=blogpost&amp;utm_medium=pr&amp;utm_campaign=devblogs&amp;utm_content=">io.google</a>.</div>

### Android CLI Now Stable 1.0: Accelerate developing for Android using any agent (Google Play)
- **Published**: 2026-05-19T11:07:45.463-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/05/android-cli-stable-1-0-agent-development.html](https://android-developers.googleblog.com/2026/05/android-cli-stable-1-0-agent-development.html)
- **Key Topics**: Google Play AI policies, AI-generated content disclosures
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjVLU7gkfsf4axphzvtOKcqEkI3MLKZqX6Y9jGVReW6Ximz61c8klVVc0_Xs5Fw_aqk5yjl3K-Mit6cyKq0SLOJbUhUZ7R3dZZcwShqn5jYp-DuHY8hNoBWHJkicoIJ9DKRINQt6seAB3s2mcwANFYX9k0scYyCgfIYQrof7ImxOvzEW7BNj0ZPwEGB5FI/s2048/GoogleForDevelopers-AndroidCombo3-StrapiMetacard-2048x1323%20(1).png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjVLU7gkfsf4axphzvtOKcqEkI3MLKZqX6Y9jGVReW6Ximz61c8klVVc0_Xs5Fw_aqk5yjl3K-Mit6cyKq0SLOJbUhUZ7R3dZZcwShqn5jYp-DuHY8hNoBWHJkicoIJ9DKRINQt6seAB3s2mcwANFYX9k0scYyCgfIYQrof7ImxOvzEW7BNj0ZPwEGB5FI/s2048/GoogleForDevelopers-AndroidCombo3-StrapiMetacard-2048x1323%20(1).png" style="display: none;" />





<div><div class="separator" style="clear: both; text-align: left;"><i>Posted by Simona Milanovic and Ben Trengrove, Developer Relations Engineers</i><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh-DNQCYynOZTPwB7Two8HSejPtcinJWir0-t4Wseo9MFHwLNeluQqIbf-9XDJXcSTaHBoX7NJ6oTFRUczPaokekC-oFEFgdZwxngaskLaxyqCGy5-ZbT0QAnmRafTvx3PKPaMo-npHZuwUAi84AW-28rWw6_2BTWHnXoXqbSrX6Kboz0fy5lz9YogDFf0/s4209/GoogleForDevelopers-AndroidCombo3-Blogger-4209x1253.png" style="clear: left; display: inline; margin-bottom: 1em; margin-right: 1em; text-align: center;"><img border="0" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh-DNQCYynOZTPwB7Two8HSejPtcinJWir0-t4Wseo9MFHwLNeluQqIbf-9XDJXcSTaHBoX7NJ6oTFRUczPaokekC-oFEFgdZwxngaskLaxyqCGy5-ZbT0QAnmRafTvx3PKPaMo-npHZuwUAi84AW-28rWw6_2BTWHnXoXqbSrX6Kboz0fy5lz9YogDFf0/s16000/GoogleForDevelopers-AndroidCombo3-Blogger-4209x1253.png" /></a></div></div><div><br /></div><div>
As Android developers, you have many choices when it comes to the agents, tools, command-line interfaces (CLI), and LLMs you use for app development. Whether you use Gemini in Android Studio,  Antigravity 2.0, Antigravity CLI, or third-party agents like Anthropic's Claude Code or OpenAI'sCodex, our mission remains the same: to ensure that high-quality Android development is possible everywhere.

  <p style="text-align: center;"><span></span></p>
<p style="text-align: center;"><span></span></p>
<div class="separator" style="clear: both; text-align: center;">
    <div style="height: 0px; max-width: 100%; overflow: hidden; padding-bottom: 56.25%; position: relative;">
        <iframe allowfullscreen="" class="BLOG_video_class" height="266" src="https://www.youtube.com/embed/aqmpZocmR8o?autoplay=1&amp;mute=1&amp;loop=1&amp;playlist=aqmpZocmR8o&amp;modestbranding=1&amp;rel=0" style="border: 0; height: 100%; left: 0; position: absolute; top: 0; width: 100%;" width="320" youtube-src-id="aqmpZocmR8o"></iframe></div></div>
<p></p>

  <p>At <b>Google I/O ‘26</b>, we shared the latest leaps forward in agentic development, and showcased some of the newest capabilities of <a href="https://developer.android.com/tools/agents/android-cli">Android CLI</a>—now stable at version 1.0 and ready for all Android developers to use. From new skills to enabling agent access to powerful Android Studio capabilities, we’re giving your agents the right tools to build alongside you.</p>

  <div style="text-align: left;">If you’re already using Android CLI and want to jump into using all the new features, just run <span style="font-family: inherit;"><code>android update<code></code></code></span>. Otherwise, read further to learn more about how we’re making the agents you choose be better at building for Android.</div>

  <h3>Android development unlocked for Antigravity</h3>
  <p><a href="https://antigravity.google/">Google Antigravity</a> now includes an optional bundle of Android resources—including the Android CLI and skills—that you can install. You can either install the bundle during onboarding after installation, or later from the <b>Settings &gt; Customizations &gt; Build With Google Plugins</b> menu.</p><p>This provides Antigravity with all the powerful tools and knowledge of Android CLI, enabling it to perform the core tasks necessary for Android app development more easily and efficiently—from creating projects to deploying your app on a new Android virtual device.</p><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEivI2fhgZRJRpz8TXcX4OC2CALzgOfHhKyVmVG0IaMsibqaAUVbZORx-5fbVrYUKlp0Fl1qk1wZ02jbrYSfFGRCtOvnOzWWYdw8G3or9ul_QY2yvT6Wm-kEIjAJtfj75kNWlSswAqoUCLvSefnFY3JMw7NQOA8hkDn3nc232oyEK1VN5ZM_UHbAEJWolWE/s16000/agy-android-cli%20(1).png" /></div><i><div style="text-align: center;"><i>You can now easily install Android CLI for use with Google Antigravity 2.0.</i></div></i><h3 style="text-align: left;">Unlocking Android Studio capabilities for any agent</h3><p>Android CLI provides a lightweight interface for AI Agents to perform tasks and retrieve knowledge about Android development. However, there's benefits to specialization — Android Studio contains over a decade of Android expertise, built to handle even the most complex Android projects. This includes Android Studio's powerful static analysis engine, refactoring tools, dependency management, UI design and rendering libraries, and more. AI Agents can now tap into Android Studio's tools to gain many of these same capabilities.</p><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhRp6RfqiD9adFdIQS9Fm_a3p_5X6K5Fjo5rEQhOeOqFpvjlQ-04DHav5atkLF7IZvnpdMaQqG_oBAhmcvCPRtAvsW7AH0Q3VF18y-TBUITLXBglNbR2o99sC-hJgj_D-OhF51rLO_OYi1RXdm6GBfgZqfsTdQa1CY6_g10D2LwLun3S1CjfqOY2pqp02Y/s16000/agy-android-studio%20(1).png" /></div><div style="text-align: center;"><i>Your agents can now use Android CLI to access powerful capabilities of Android Studio.</i></div><p>The latest version of Android CLI introduces the new <code>android studio</code> command. This enables the agent of your choice to leverage the deep, contextual capabilities of Android Studio to better understand and perform actions on an open Android project. By running Android Studio alongside your preferred agent with Android CLI, your agent’s tasks can more efficiently navigate the codebase to produce more precise code changes. And, when you use Android CLI to create and iterate on your project, transitioning to Android Studio is much easier, so that you can use the purpose built tools—such as, performance profilers, Compose Previews, and Android Device Streaming—to get that production-grade polish.</p>

  <p>When you have a project open in the latest <a href="https://developer.android.com/studio/preview">preview version</a> of Android Studio Quail, you (or your agent) can run the following command to check whether Android CLI has a connection established with your open project:</p>

<pre><span id="docs-internal-guid-dae0cd34-7fff-1f39-ceb6-adffcef2b792"><p dir="ltr" style="line-height: 1.2; margin-bottom: 0pt; margin-top: 0pt;"><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">$ android studio check</span></p><p dir="ltr" style="line-height: 1.2; margin-bottom: 0pt; margin-left: 36pt; margin-top: 0pt;"><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">pid: </span><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; font-weight: 700; vertical-align: baseline; white-space: pre-wrap;">32942</span></p><p dir="ltr" style="line-height: 1.2; margin-bottom: 0pt; margin-left: 36pt; margin-top: 0pt;"><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">version: </span><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; font-weight: 700; vertical-align: baseline; white-space: pre-wrap;">Android Studio</span></p><p dir="ltr" style="line-height: 1.2; margin-bottom: 0pt; margin-left: 36pt; margin-top: 0pt;"><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; font-weight: 700; vertical-align: baseline; white-space: pre-wrap;">Projects:</span></p><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; font-weight: 700; vertical-align: baseline; white-space: pre-wrap;">READY</span><span style="color: #188038; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;"> &nbsp; &nbsp; JetSet /Users/adarshf/AndroidStudioProjects/jetset-main</span></span></pre>

  <p>From there, the agents can use the <code>android studio</code> command to access powerful IDE tools to interact with projects more efficiently. Key commands include:</p><p></p><ul style="text-align: left;"><li><b>analyze-file:</b> Analyzes a file for errors and warnings using the editor's built-in inspections.</li><li><b>find-declaration:</b> Finds the exact definition site of a symbol (class, method, variable, field, constant, or Android resource/color) across the project using semantic resolution.</li><li><b>find-usages: </b>Finds all references and declarations of a symbol (class, method, variable, or Android resource) across the entire project using semantic analysis.</li><li><b>render-compose-preview: </b>Renders a Jetpack Compose UI Preview and returns a path to the image and UI hierarchy if successful.</li><li><b>version-lookup:</b> Get the latest information about which versions for specified app dependencies are available in common repositories, such as the Google Maven repository. By providing a programmatic solution, dependency management is less tedious and much less prone to flakiness.</li><li><b>open-file: </b>Opens a file directly in Android Studio. This is useful if the agent wants to direct your attention to view Compose Previews, performance traces, or other specific files in the IDE.</li></ul><p></p><ul>
  </ul>

  <p>For example, agents can now run the following commands to render a Compose preview for a new layout for your Android app, and then open the previews in Android Studio for you to take advantage of seeing multiple Compose Previews side by side and make AI-assisted edits right from the IDE.</p>

<pre><span id="docs-internal-guid-e7668cd3-7fff-aabf-baa3-bfe1ea7196b7"><p dir="ltr" style="line-height: 1.2; margin-bottom: 0pt; margin-top: 0pt;"><span style="color: #37474f; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">$ android studio </span><span style="color: #37474f; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; font-weight: 700; vertical-align: baseline; white-space: pre-wrap;">find-declaration</span><span style="color: #37474f; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;"> HotelDetailScreen</span></p><p dir="ltr" style="line-height: 1.2; margin-bottom: 0pt; margin-top: 0pt;"><span style="color: #37474f; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">$ android studio </span><span style="color: #37474f; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; font-weight: 700; vertical-align: baseline; white-space: pre-wrap;">analyze-file</span><span style="color: #37474f; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;"> .../JetPacker/feature/detail/src/main/java/com/example/jetset/feature/detail/HotelDetailScreen.kt</span></p><span style="color: #37474f; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;">$ android studio </span><span style="color: #37474f; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; font-weight: 700; vertical-align: baseline; white-space: pre-wrap;">open-file</span><span style="color: #37474f; font-family: &quot;Roboto Mono&quot;, monospace; font-size: 9pt; font-variant: normal; vertical-align: baseline; white-space: pre-wrap;"> feature/detail/src/main/java/com/example/jetset/feature/detail/HotelDetailScreen.kt</span></span></pre>

  <p>To learn more about how to use these commands, run <code>android help</code>. And, to make sure your agents understand how to work with this tool, make sure to update the Android CLI skill by running <code>android init</code>.</p>

  <h3>More ways to get started</h3>
  <p>To make integrating Android CLI into your environments as seamless as possible, we’re making it available in more ways. You can now download and install Android CLI using more package managers: apt-get, winget, and homebrew. For example, you can run the following to install Android CLI using winget:</p>

  <pre>winget install -e --id Google.AndroidCLI</pre>

  <p>We’ve also updated the installation to a user-local directory, by default. You can find the commands for all supported operating systems plus additional download options on the <a href="https://developer.android.com/tools/agents/android-cli/archive">Android CLI page</a>.</p>

  <h3>Support for Journeys</h3>
  <div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEip7lO5BVjTIeJXDWyrGOdl4KpPTo8_oEcf0qLFUBRfPgOazlG7C9eLWDLdnNYb68-rlon4uOE4qo62WC_U7SaAOYwLG3Vbr0v_lRsh-iNoPzVMmFbAgKXXN1hz9Qj7rMImyybqHCU34ryMlml2fCquAyfNgp1yWiZu-CsP1Jowx4o0z69_wkNtYR0GQIM/s16000/android-cli-write-journey.png" /></div><div style="text-align: center;"><i>Journeys are natural language descriptions of core user experiences.</i></div><div><br /></div><p>&nbsp;</p><div class="separator" style="clear: both; text-align: center;"><img border="0" data-original-height="576" data-original-width="960" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjeAW4kjqfV1t_mAw_iYwgWSczw3q-h3VEOAuDAe12uBel0niX6M2KAoGrs6M2UHhT3t1GvBZs-c3w0R87W6HgCAzHQZOdFjixUHyYCZRzhOgB_RtOkVh0Ph8cDFki0sWI8i5CFNXxGxBHai0uh0RZw5E9kcJUvl8DJtPT3tnkaQm5r8UHuWMstopnTnnI/s16000/android-cli-journey-run.gif" /></div><p style="text-align: center;"><i>(sped up) An agent running a Journey it generated for an app.</i></p>Agents can run these journeys using the Android CLI to navigate your app exactly like a user would. This unlocks entirely new ways to test, validate, or collect data across the critical experiences of your app, all driven by natural language and executed by your agent.

  <h3>Expanding Android skills</h3>
  <p>To help models better understand and execute specific patterns that follow our best practices, we are continuing to expand our <a href="https://github.com/android/skills">library of Android skills</a>. We’re shipping new skills that make Android development everywhere more capable, efficient, and productive:</p><p></p><ul style="text-align: left;"><li><b>Display Glasses and Jetpack Compose Glimmer for XR: </b>Provides guidelines for developing projected applications for Android Display Glasses using the Jetpack Compose Glimmer UI toolkit.</li><li><b>Migration to CameraX:</b> Helps you migrate legacy Android camera implementations (Camera1 or raw Camera2 APIs) to CameraX.</li><li><b>Perfetto SQL:</b> Translates natural language data prompts into Perfetto SQL queries and executes them against a local trace file.</li><li><b>Adaptive UI:</b> Instructions to make or update an app's UI so that it adapts to different Android devices</li><li><b>Testing setup: </b>Creates a basic testing strategy.</li><li><b>Styles:</b> Helps with adoption of the new Jetpack Compose Style API for new components, and supports migration to Styles API.&nbsp;</li><li><b>AppFunctions: </b>Analyzes Android codebases to recommend and implement new AppFunctions, and refines KDoc documentation for Model Context Protocol optimization.</li></ul><p></p><p>You can add these new skills to your workflow directly from the command line. To help your agents understand and use Android CLI right away, you can initialize your environment and install the base android-cli skill by running:</p>
<pre>android init
</pre>
  <p>From there, you can browse and set up your agent workflow by searching for the exact capabilities your agent needs:</p>
<pre>android skills list
</pre>
  <p>Once you've found the right skill, install it to your environment by running:</p>
<pre>android skills add –skill=&lt;skill-name&gt;
</pre>

  <h3>Get started today</h3>
  <p>To download the stable 1.0 release of the Android CLI, explore the new tools, and browse the complete documentation, head over to <a href="https://d.android.com/tools/agents">d.android.com/tools/agents</a> today!&nbsp; Also, make sure you update to the <a href="https://developer.android.com/studio/preview">latest preview version of Android Studio</a> to unlock the latest features that Android CLI offers. We can't wait to see what you build with Android CLI 1.0 and how these new features supercharge your daily workflows. Join our vibrant community on <a href="https://www.linkedin.com/showcase/androiddev/posts/?feedView=all">LinkedIn</a>, <a href="https://medium.com/androiddevelopers">Medium</a>, <a href="https://www.youtube.com/c/AndroidDevelopers/videos">YouTube</a>, or <a href="https://twitter.com/androidstudio">X</a> and&nbsp; share your feedback.</p><p>Explore this announcement and all Google I/O 2026 updates on <a href="https://io.google/2026/?utm_source=blogpost&amp;utm_medium=pr&amp;utm_campaign=devblogs&amp;utm_content=">io.google.</a></p></div>

### Build for the future with the Android XR Developer Catalyst Program — Apply now! (Google Play)
- **Published**: 2026-05-19T11:14:13.068-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/05/apply-android-xr-developer-catalyst.html](https://android-developers.googleblog.com/2026/05/apply-android-xr-developer-catalyst.html)
- **Key Topics**: General Google Play AI policy
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiY7FqaPopxHI3Dq1hBDIMB81rZ59f1qF4MjvryAoYitMFpbQNgi6PElj8QSUNHHIZSmv1aX4Dt-UMAmoGtmowcpd4gf-TWNdKEPk_eeCErg7O5X3GwIKw4GZ4x06iJERPYHik0QPuO50LiMyiLxzCVgm-gFUJfUBAjFqRlrUnJgNV7NwnYZYyrr7_t0M0/s2048/GoogleForDevelopers-AndroidText-StrapiMetacard-2048x1323.png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiY7FqaPopxHI3Dq1hBDIMB81rZ59f1qF4MjvryAoYitMFpbQNgi6PElj8QSUNHHIZSmv1aX4Dt-UMAmoGtmowcpd4gf-TWNdKEPk_eeCErg7O5X3GwIKw4GZ4x06iJERPYHik0QPuO50LiMyiLxzCVgm-gFUJfUBAjFqRlrUnJgNV7NwnYZYyrr7_t0M0/s2048/GoogleForDevelopers-AndroidText-StrapiMetacard-2048x1323.png" style="display: none;" />




<div class="separator" style="clear: both; text-align: left;">Posted by Android XR Team</div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjK-8uaBuG-Xdug5wfik0xw8C-Nhyphenhyphenj5-Z7tHoQjxeFwH-5qqg2OB2DSGMHgHFd_372Fx_tREZxL51mDBFJEGMpc5eH9bH-7461bXKEXZgefVhPAmAU8Ehvk8_zpnkhODFFI51tyrJMnoudf3a6b9sCfEqcJoZ-idYpBVVUet8Ehc2gUR30R2D8ADSS-RdE/s4209/GoogleForDevelopers-AndroidText-Blogger-4209x1253.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjK-8uaBuG-Xdug5wfik0xw8C-Nhyphenhyphenj5-Z7tHoQjxeFwH-5qqg2OB2DSGMHgHFd_372Fx_tREZxL51mDBFJEGMpc5eH9bH-7461bXKEXZgefVhPAmAU8Ehvk8_zpnkhODFFI51tyrJMnoudf3a6b9sCfEqcJoZ-idYpBVVUet8Ehc2gUR30R2D8ADSS-RdE/s16000/GoogleForDevelopers-AndroidText-Blogger-4209x1253.png" /></a></div><br /><div><br /></div>
<div><br /></div>
<div>
  <p dir="ltr">The Android XR ecosystem is expanding, and we’re committed to supporting developers who will build its next great experiences. Today, we’re opening applications for the <a href="http://developer.android.com/develop/xr/catalyst">Android XR Developer Catalyst Program</a>, a dedicated initiative to accelerate the development of Android XR apps ready to launch within the next year.</p>

  <p dir="ltr">This program is designed to provide the resources, hardware, and grants to help you build and scale innovative experiences across <a href="https://developer.android.com/develop/xr/devices#xr-glasses">wired XR glasses</a>, like <a href="https://www.xreal.com/us/aura">XREAL’s Project Aura</a>, and <a href="https://developer.android.com/develop/xr/devices#audio-display">intelligent eyewear</a>&nbsp;(audio and display glasses). We are especially interested in seeing innovative experiences across media, gaming, productivity, and health, but we welcome any unique use case that helps users expand what's possible.</p>

  <h3 dir="ltr">Why join the catalyst program?</h3>

  <p dir="ltr">We want to help developers navigate common barriers to entry for XR development by providing:</p>

  <ul>
    <li dir="ltr">
      <p dir="ltr"><strong>Development Kits:</strong> Get early access to hardware development kits for wired XR glasses (XREAL’s Project Aura) and / or intelligent eyewear (audio and display glasses).</p>
    </li>
    <li dir="ltr">
      <p dir="ltr"><strong>Technical support:</strong> Gain access to specialized technical resources and support forums specifically designed to help you prepare your app for Google Play.</p>
    </li>
    <li dir="ltr">
      <p dir="ltr"><strong>Grant Opportunities:</strong> Submit a request and you may be eligible to receive a non-recoupable grant to accelerate your development.</p>
    </li>
  </ul>

  <h3 dir="ltr">Ready to start building?</h3>

  <p dir="ltr">Applications are open to developers looking to publish apps for the Android XR ecosystem in the next 6-12 months. You can build with Kotlin and the <a href="https://developer.android.com/develop/xr/jetpack-xr-sdk">Jetpack XR SDK</a>, or with <a href="https://developer.android.com/develop/xr/unity">Unity</a>, <a href="https://developer.android.com/develop/xr/unreal">Unreal Engine</a> or <a href="https://developer.android.com/develop/xr/godot">Godot</a>. If you need a spark of inspiration, you can check out existing XR <a href="https://developer.android.com/develop/xr/experiments">Experiments</a> and <a href="https://developer.android.com/develop/xr/samples">Samples</a> to see how you can use the SDK for everything from spatial music to navigation.</p>

  <p dir="ltr">Once you have your concept ready, be sure to <a href="http://developer.android.com/develop/xr/catalyst">submit your application</a> by June 30th by 11:59PM PDT. We can’t wait to see what you build.</p>

  <p dir="ltr"><strong><a href="http://developer.android.com/develop/xr/catalyst">Start Your Application</a></strong></p><p dir="ltr">Explore this announcement and all Google I/O 2026 updates on&nbsp;<span style="display: none;"></span><a href="https://io.google/2026/?utm_source=blogpost&amp;utm_medium=pr&amp;utm_campaign=devblogs&amp;utm_content=" rel="noopener nofollow noreferrer" target="_blank">io.google<span style="display: none;"></span></a>.</p>
</div>

### Adaptive development for the expanding Android ecosystem (Google Play)
- **Published**: 2026-05-19T11:07:17.914-07:00
- **Official Link**: [https://android-developers.googleblog.com/2026/05/android-adaptive-development-ecosystem.html](https://android-developers.googleblog.com/2026/05/android-adaptive-development-ecosystem.html)
- **Key Topics**: Google Play AI policies
- **Details**: <meta content="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhdDsacfyGtp3onpFDB8MfwDNaY70RiTJpN0e_M0NK9W7au1Ex8ghyphenhyphenGNrIq0sqqc1eb-g2fUPUYL1sS7Fhk5r7GTDZm3p-3gRDulDyPa0RqLcDXk6uV3TjBpLMDU5RMnvySqazjwL-8dKrrjkfqkgM_ODlmZVgGNnX5e067nNgWL146AHbsejj6KtLrtIs/s2048/GoogleForDevelopers-ComboIO-StrapiMetacard-2048x1323%20(1).png" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"></meta>
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhdDsacfyGtp3onpFDB8MfwDNaY70RiTJpN0e_M0NK9W7au1Ex8ghyphenhyphenGNrIq0sqqc1eb-g2fUPUYL1sS7Fhk5r7GTDZm3p-3gRDulDyPa0RqLcDXk6uV3TjBpLMDU5RMnvySqazjwL-8dKrrjkfqkgM_ODlmZVgGNnX5e067nNgWL146AHbsejj6KtLrtIs/s2048/GoogleForDevelopers-ComboIO-StrapiMetacard-2048x1323%20(1).png" style="display: none;" />


<div><div class="separator" style="clear: both; text-align: left;"><i>Posted Fahd Imtiaz, Senior Product Manager, Adaptive Apps</i></div></div><div><div class="separator" style="clear: both; text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEieeKKXz0dxJIT708pHha_v_9k68Z78o4aDP1ZXktjSjhOKOe64zs5x0iL07nab5_X2EYWLsxGYgVFu-SAS_U4BFkHUOudIj_GeIllKeNFiZys_5wFVh52UXvI2NPz1RmCvaIHsSqJCT0pd2-LhUFig1Xcn6n7Bl9nTb0P-jjpSXBkOR3fM5zzv_H8ljIM/s4209/GoogleForDevelopers-ComboIO-Blogger-4209x1253.png" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="1253" data-original-width="4209" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEieeKKXz0dxJIT708pHha_v_9k68Z78o4aDP1ZXktjSjhOKOe64zs5x0iL07nab5_X2EYWLsxGYgVFu-SAS_U4BFkHUOudIj_GeIllKeNFiZys_5wFVh52UXvI2NPz1RmCvaIHsSqJCT0pd2-LhUFig1Xcn6n7Bl9nTb0P-jjpSXBkOR3fM5zzv_H8ljIM/s16000/GoogleForDevelopers-ComboIO-Blogger-4209x1253.png" /></a></div><br /><i><br /></i><div><i><br /></i><div>With the release of Android 17, we are transitioning into an <a href="https://developer.android.com/adaptive-apps">adaptive first development</a> standard. Your users no longer rely on a single form factor; they transition between phones, foldables, tablets, laptops, automotive displays, and immersive XR environments throughout their day.

  <p dir="ltr">Now, with over <strong>580 million large screen devices</strong> in the hands of users, adaptive is no longer just a technical goal. It’s a massive opportunity to reach highly engaged users. To thrive in this multi-device ecosystem, your app must be resilient, responsive, and ready for virtually any surface.</p>

  <h3 style="text-align: left;">The multi-device opportunity</h3><p dir="ltr">The Android device universe is now a multi device reality. Users are buying into entire ecosystems, moving from handhelds to foldables, tablets, and cars. And the data is clear: users with multiple devices often spend more than users with only a phone.</p>

  <ul>
    <li dir="ltr">
      <p dir="ltr"><strong>Drive higher revenue:</strong> Multi-device users spend <strong>9x more</strong> on average than phone only users. On foldables, that engagement multiplier can reach 14x. <i>(Source: Google Internal Data, 2026)</i></p>
    </li>
    <li dir="ltr">
      <p dir="ltr"><strong>Capture high-value segments:</strong> Large-screen users (tablets, foldables, and Chromebooks) typically spend roughly <strong>5x more</strong> than phone-only users.</p>
    </li>
  </ul>

  <p dir="ltr">To help amplify your reach with these users, we've rolled out a new badge in Google Play. Apps meeting adaptive quality standards now earn an "Optimized for large screens" badge, making it easier for users to discover high quality experiences.</p>

  <p dir="ltr" style="text-align: center;">
    <img src="https://blogger.googleusercontent.com/img/a/AVvXsEj8tcHEiqfZumSLdhBppKYl9Ue3umyMqjU5efDFWp0Tz2W6Ng_-gZQd8VHD6Vekv1MqR5W741NdcMOLS-Mdpe8LAYurPGl429pHRY99vTyAYWI2h6NZP4QCi8mT4_d7GJZcExwJFSQ2e7Iyyw_YS4t297I4eNyIIreH2tu0kgr2LxBPB1LyBDDMZ8pUJzQ" style="height: auto; max-width: 100%;" title="Frame 2134283034 (2).png" />
  </p>

  <h3 style="text-align: left;">Latest in adaptive Android development from Google I/O</h3><p dir="ltr">Android 17, new Jetpack updates and advanced tools help you build apps that feel native across diverse surfaces, from pocket-sized foldables to <a href="https://developer.android.com/googlebook">Googlebooks</a>.</p>

  <b>Adaptive by default: Android 17 updates</b>

  <p dir="ltr">In Android 16, we <a href="https://android-developers.googleblog.com/2025/01/orientation-and-resizability-changes-in-android-16.html">introduced significant changes</a> to orientation and resizability APIs to facilitate adaptive behavior, while providing a temporary opt-out to help you make the transition. Android 17 (API level 37) sets a new quality baseline by removing that developer opt-out for orientation and resizability restrictions on large screen devices (sw &gt; 600 dp). When you target API level 37, your app must be capable of adapting to a variety of display sizes. This helps your app deliver an experience that matches the users’ expectations.</p>

  <p dir="ltr" style="text-align: center;">
    <img alt="Apps that were previously letterboxed on large screen devices will now be stretched to landscape" src="https://blogger.googleusercontent.com/img/a/AVvXsEhpP-QNEuXvCQhSF7XX_HDsnbStMuQLxFNDrSd_k2mQB-cjs494xAMZg3yO6l3zCt6N9q34tekmQ7ILIa8JuKbI-QgkDm0XDfyuajeM2q32QtzieneZG7vedfQoythMS-Di9V0g3ung6BDTD3UPZMANMpifh5Vpwi049Uhqr-Gyx6D6gO6QUjtVd8MemlQ" style="height: auto; max-width: 100%;" />
  </p>

  <p dir="ltr"><i>Tip: You can start testing these behaviors by enabling the UNIVERSAL_RESIZABLE_BY_DEFAULT flag in App Compatibility Changes under Developer Options under SDK 36.</i></p>

  <b>Your app on even more surfaces</b>

  <p dir="ltr">In addition to your mobile app running on large screens devices including foldables, tablets, Chromebooks and XR, we are also expanding the Android surface area for your mobile apps:</p>

  <ul>
    <li dir="ltr">
      <p dir="ltr"><strong>Connected Displays:</strong> Now in stable as of Android 16 QPR3, Connected Displays support enables supported Pixel and Samsung mobile devices to transform into a desktop environment via external display support.</p>
    </li>
    <li dir="ltr">
      <p dir="ltr"><strong>Automotive &amp; TV:</strong> With the <a href="https://developer.android.com/training/cars/car-ready-mobile-apps">Car Ready Mobile Apps program</a> and enhanced <a href="http://android-developers.googleblog.com/2026/05/increase-google-tv-app-discovery.html">pointer support for Android TV</a>, your adaptive app can now benefit from engagement on the infotainment system and the living room with ease.</p>
    </li>
  </ul>

  <p dir="ltr" style="text-align: center;">
    <img src="https://blogger.googleusercontent.com/img/a/AVvXsEjKyoQ_8VV6z8raeEbcAx_imJtuRs6I7wKHkAhG7JieTpewDH1eoiPp6UIfSZSzdtsMbO9_UfSHhUOcK3vJBePxxoBzkwUwl0QaUQ9wFtZIfhtdVLwBlIzCzM8FzOqoZAyI0jEHmhj6esXqZICOQsT5SXZcG2kLL6DVFv1_hzz_F7xZ70eXsEZVEZGzeNc" style="height: auto; max-width: 100%;" />
  </p>

  <b>Googlebook: Evolving desktop computing</b>

  <p dir="ltr">Talking about more surfaces, we’re evolving our work in the desktop space with Googlebook, the next generation of ChromeOS. Built with parts of the Android stack, we are enabling your apps to achieve a "laptop-class" feel with native level performance.</p>

  <p dir="ltr">Building with adaptive principles today helps ensure your app is ready for this new generation of high performance hardware.</p>

  <p dir="ltr">To help you prepare for this new generation of devices, we’ve released comprehensive new documentation including comprehensive <a href="https://developer.android.com/design/ui/desktop">design guidance</a> and <a href="https://developer.android.com/docs/quality-guidelines/adaptive-app-quality/experiences/desktop">developer guidelines</a>. Built on the principles of adaptive, these guidelines offer a playbook for transitioning your mobile apps to offer a premium desktop class experience.</p>

  <p dir="ltr">Try out the new Desktop Emulator, available now in the Android Studio Canary to get started today.</p>

  <div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhgdC6ILILt8u8MeVRwqEd137F8RbiSYJUgE68W7mrgRkm5T2biCFrSfsEA4yUu45yUqvy3MCw22r4lcxqwXe1KTnLzbFO0i7QyvYSstKAHObGzBT4cUmIIzYqIyV2lt45Cn1FCQ4KYl-QgOx0XH2fyFVOq8B_vVnvbLKnJ8AzXFEzaXAEcCFybdNHlGMI/w400-h400/google_aluminium_hype_film_hp_sh18019_main_design_v04_00068.png" /></div>

  <b><div><b><br /></b></div>Building adaptive layouts with Jetpack Compose</b>

  <p dir="ltr">We are now <a href="https://goo.gle/Compose_IO26">Compose first</a> and Jetpack Compose is our recommended way to build modern, adaptive UIs to help you manage layout complexity efficiently.</p>

  <ul>
    <li dir="ltr">
      <p dir="ltr"><strong>New layout primitives:</strong> We’re introducing <a href="https://developer.android.com/develop/ui/compose/layouts/adaptive/grid">Grid</a> and <a href="https://developer.android.com/develop/ui/compose/layouts/adaptive/flexbox">FlexBox</a> layouts, bringing powerful, CSS-inspired capabilities to Compose for both 1D and 2D layouts.</p>
    </li>
    <li dir="ltr">
      <p dir="ltr"><strong>Navigation 3:</strong> The <a href="https://developer.android.com/jetpack/androidx/releases/navigation3">1.1 release</a> for compose-navigation3 introduces <a href="https://developer.android.com/guide/navigation/navigation-3/scenes/scene-decorators">Scene Decorators</a>, allowing you to wrap your screens with other content, such as bars, rails and dialogs.</p>
    </li>
    <li dir="ltr">
      <p dir="ltr"><strong>MediaQuery API:</strong> The new experimental <a href="https://developer.android.com/reference/kotlin/androidx/compose/ui/mediaQuery.composable?hl=en">MediaQuery API</a> provides observable device UI capabilities, such as window size and pointer precision, that allow you to adapt and optimize your app's UI for the current device configuration.</p>
    </li>
    <li dir="ltr">
      <p dir="ltr"><strong>Styles API:</strong> Dynamically evolve the visual properties of your app using the new state-based experimental <a href="https://developer.android.com/develop/ui/compose/styles">Styles API</a>.</p>
    </li>
  </ul>

  <div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjWrhxL-9SuZTgfd5LS2TeEU5NS_F0h4U_zzK59koOU-CenOLFpCrFs80-RHP1mC_qfAzLeqgYkgVhfOeZpMtNTAvivGR8DpYLL61oVsuhAjI-pTYrXw21pW2Ec8JAmG9vIwDks70XpSSv8wiJiGaK95PQ1Kn_kEdmUbW401-XAsLBEIDlG_k5c5BTtzU4/w640-h414/morph-to-tablet%20(1).gif" /></div>

  <b>Beyond layouts: non-touch input</b>

  <p dir="ltr">Adaptive app quality goes beyond window dimensions, including handling non-touch input paradigms e.g. keyboard, trackpad, mouse, stylus that are primary input methods on large screens.</p>

  <ul>
    <li dir="ltr">
      <p dir="ltr"><strong>Trackpad support:</strong> <a href="https://developer.android.com/blog/posts/whats-new-in-the-jetpack-compose-april-26-release">Compose 1.11</a> now brings trackpad support on par with mouse, and provides new APIs to automate non-touch input testing including <code>TrackpadInjectionScope</code> and <code>performTrackpadInput</code>.</p>
    </li>
    <li dir="ltr">
      <p dir="ltr"><strong>Focus indicators:</strong> Enhance accessibility with built-in support for standard focus rings in Compose.</p></li>
  </ul>

  <b><div><b><br /></b></div>AI-Powered developer tools</b>

  <p dir="ltr">Android Studio and <a href="https://developer.android.com/tools/agents/android-cli">Android CLI</a> are evolving to help you architect adaptive apps faster than ever.</p>

  <ul>
    <li dir="ltr">
      <p dir="ltr"><strong>Android Skills:</strong> These modular AI instructions are designed to assist any LLM through complex architectural tasks, including helping you with View-to-Compose migrations, implementing adaptive layouts, Navigation 2 to Navigation 3 transformation, and migrating off of legacy camera libraries to CameraX. Get started with these latest skills on the Android Skills <a href="https://github.com/android/skills">Github repo</a> and <a href="https://developer.android.com/tools/agents/android-cli#skills-add">via Android CLI.</a></p>
    </li>
    <li dir="ltr">
      <p dir="ltr"><strong>New Project Agent:</strong> Available in Android Studio Panda 2, this agent initializes new projects with adaptive best practices by default.</p>
    </li>
  </ul>

  <br />

  <p dir="ltr"></p><div class="separator" style="clear: both; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhK9P3KbiU-qqzVx45wLUsYxGySpAeBaEiaxH6fJawNowXhJd8jdcMvBQ-62ejoHOz9de-MAdCEsmISI4ntqUI8ANeZjm0TqFNu0bEKyBsCbrsdPhVwupTEVfMasvegiyDrz4hSH3cxte-EMIWY0lpxFfg9OBqLhImBLlmZ8jXa3VOwvbo7_TG9gRUXXf0/s16000/Copy%20of%20IO26_315_PKLS%20-%20Adaptive%20development%20for%20the%20expanding%20Android%20ecosystem%20-%20Deck%20(1).png" /></div>For developers working with cross-platform frameworks, we continue to provide full support for Web, Qt, and Unity. Whether you are building from scratch or modernizing a legacy codebase, these tools are designed to meet your users exactly where they are.<p></p>

  <p dir="ltr">We’re excited to see how you bring these new adaptive capabilities to your apps. By moving to an adaptive first approach, you’re not just reaching more users but you’re delivering the seamless, high quality experiences they expect across the entire Android device landscape.</p>

  <p dir="ltr">Get started with <a href="https://developer.android.com/adaptive-apps">adaptive development</a> and start shaping the future of your apps.</p><p dir="ltr">Explore this announcement and all Google I/O 2026 updates on <a href="https://io.google/2026/?utm_source=blogpost&amp;utm_medium=pr&amp;utm_campaign=devblogs&amp;utm_content=">io.google</a>.</p>
</div><br /></div></div>

<!-- AI_POLICY_MONITOR_END -->