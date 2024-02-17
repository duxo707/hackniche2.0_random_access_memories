
import './App.css';
import gptLogo from './assets/chatgpt.svg';
import addbtn from './assets/add-30.png';
import msgIcon from './assets/message.svg';
import home from './assets/home.svg';
import saved from './assets/bookmark.svg';
import rocket from './assets/rocket.svg';
import sendBtn from './assets/send.svg';
import userIcon from './assets/user-icon.png';
import gptImgLogo from './assets/chatgptLogo.svg';
function App() {
  return (
    <div className="App">
      <div className='sidebar'>
        <div className='upperSide'>
            <div className='upperSideTop'><img src={gptLogo} alt='' className='logo' /> <span className='brand'>Hack</span></div>
            <button className='midBtn'><img src={addbtn} alt='' className='addBtn' />New Chat </button>
            <div className='upperSideBottom'>
              <button className='query'><img src={msgIcon} alt='' />What is Programming ?</button>
              <button className='query'><img src={msgIcon} alt='' />How to use an api?</button>
            </div>
        </div>
        <div className='lowerSide'>
          <div className='listItems'><img src = {home} alt = "" className='listitemsImg' /> Home</div>
          <div className='listItems'><img src = {saved} alt = "" className='listitemsImg' /> Saved</div>
          <div className='listItems'><img src = {rocket} alt = "" className='listitemsImg' /> Upgrade to Pro</div>
        </div>
      </div>
      <div className='main'>
        <div className='chats'>
          <div className='chat'>
            <img src={userIcon} />
            <p className='txt'>lorem ipsum</p>
          </div>
          <div className='chat'>
            <img src={gptImgLogo} />
            <p className='txt'>lorem ipsum</p>
          </div>
        </div>
        <div className='chatFooter'>
          <div className='inp'>
            <input type = "text" placeholder='Send a message..' />
            <button className='send'>
              <img src = {sendBtn} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
