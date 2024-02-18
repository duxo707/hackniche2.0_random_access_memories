import './BotIcon.css';

const BotIcon = () => {
    return (
        <div class="container">
            <div id="chatbot">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
            <div id="chatbot-corner"></div>
            <div id="antenna">
                <div id="beam"></div>
                <div id="beam-pulsar"></div>
            </div>
        </div>
    );
}

export default BotIcon;