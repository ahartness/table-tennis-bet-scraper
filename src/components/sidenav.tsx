import React, { useState } from 'react'
import styled from 'styled-components'
import { parseDate } from '../utils/dateconversion';

// Styled Components
const Container = styled.div`
  display: flex;
  flex-direction: row;
`;

const SideNav = styled.div`
  position: fixed;
  top: 0;
  left: ${({ isOpen }) => (isOpen ? '0' : '-250px')};
  height: 100%;
  width: 250px;
  background-color: #333;
  color: #fff;
  overflow-x: hidden;
  transition: all 0.3s ease-in-out;
  padding-top: 10px;
  z-index: 1000;

  @media (min-width: 768px) {
      display: block;
      left: 0;
    }

  ul {
    list-style-type: none;
    padding: 0;
    margin-top: 1px;

    li {
      padding: 5px 3px;
      text-align: left;
      cursor: pointer;

      &:hover {
        background-color: #575757;
      }
    }
  }
`;

const Overlay = styled.div`
  display: ${({ isOpen }) => (isOpen ? 'block' : 'none')};
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
`;

const MainContent = styled.div`
  flex: 1;
  margin-left: 250px;
  padding: 10px;
  transition: margin-left 0.3s ease-in-out;

  @media (max-width: 768px) {
    margin-left: ${({ isOpen }) => (isOpen ? '250px' : '0')};
  }

  @media (min-width: 768px) {
    margin-left: 250px;
    display: block;
  }
`;

const MenuButton = styled.button`
  position: fixed;
  top: 15px;
  left: 20px;
  z-index: 1001;
  background-color: #28a745;
  color: #fff;
  border: none;
  padding: 8px 8px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;

  &:hover {
    background-color: #28a745;
  }

  @media (min-width: 769px) {
    display: none;
  }
`;

const SideNavComponent = ({ onDataSelectionChange, jsonData, bestPlays }) => {
    const [isOpen, setIsOpen] = useState(false)
    const [activeTab, setActiveTab] = useState('all')

    const handleSelection = (value: any) => {
        onDataSelectionChange(value)
        toggleSideNav()
    }

    const handleBestPlaySelection = (value: any) => {
        const index = jsonData.findIndex((data: any) =>
            data.date === bestPlays[value].date && data.home_player === bestPlays[value].home_player && data.away_player === bestPlays[value].away_player
        );
        if (index >= -1) {
            handleSelection(index)
        }
    }

    const toggleSideNav = () => {
        setIsOpen(!isOpen)
    }

    return (
        <Container>
            <MenuButton onClick={toggleSideNav}>{isOpen ? 'Close' : 'Menu'}</MenuButton>
            <SideNav isOpen={isOpen}>
                <div style={{ width: '100%', marginTop: '60px', display: 'flex', justifyContent: 'space-around', borderBottom: '1px solid' }}>
                    <button style={{ borderTopRightRadius: '10px', borderTopLeftRadius: '10px', width: '100%', height: '100%', fontSize: 'large', backgroundColor: activeTab === 'all' ? '#28a745' : '#242424', color: activeTab === 'all' ? '#000' : '#fff' }} onClick={() => setActiveTab('all')}>All</button>
                    <button style={{ borderTopRightRadius: '10px', borderTopLeftRadius: '10px', width: '100%', height: '100%', fontSize: 'large', backgroundColor: activeTab === 'top' ? '#28a745' : '#242424', color: activeTab === 'top' ? '#000' : '#fff'}} onClick={() => setActiveTab('top')}>Top</button>
                </div>
                {activeTab == 'all' && (<ul>
                    {/* <li><h3 style={{ padding: '2px', margin: '2px', justifySelf: 'center', borderBottom: '1px solid' }}>All Plays</h3></li> */}
                    {jsonData.map((data, index) => {
                        // if (parseDate(jsonData[index]["date"]) > new Date(new Date().getTime() - 30 * 60 * 1000)) {
                            return (
                                <li style={{ borderBottom: '1px solid' }} key={index} onClick={() => handleSelection(index)}>
                                    {data["date"]} <br />{data["home_player"]}<br />{data["away_player"]}
                                    <br />
                                    {data["mean"].toFixed(2)}±{data["confidence_interval"].toFixed(2)} &nbsp;
                                    <span>[{(data["mean"] - data["confidence_interval"]).toFixed(2)} - {(data["mean"] + data["confidence_interval"]).toFixed(2)}]</span>
                                </li>
                            )
                        // }
                    })}
                </ul>)}
                {activeTab == 'top' && (
                    <ul>
                        {/* <li><h3 style={{ padding: '2px', margin: '2px', justifySelf: 'center', borderBottom: '1px solid' }}>Best Plays</h3></li> */}
                        {bestPlays.map((data, index) => {
                            // if (parseDate(bestPlays[index]["date"]) > new Date(new Date().getTime() - 30 * 60 * 1000)) {
                                return (
                                    <li style={{ borderBottom: '1px solid' }} key={index} onClick={() => handleBestPlaySelection(index)}>
                                        {data["date"]} <br />{data["home_player"]} vs.<br />{data["away_player"]}
                                        <br />
                                        {data["confidence"]} &nbsp; {data["ci_interval"]}
                                        <br />
                                        {data["last_5"]} - {data["last_10"]} - {data["last_15"]} - {data["last_20"]}
                                        <br />
                                        Hit Rate: {data["hit_rate"]}
                                        <br />
                                        Bet Amt: {data["bet_amt"]}
                                    </li>
                                )
                            // }
                        })}
                    </ul>
                )}
            </SideNav>
            <Overlay isOpen={isOpen} onClick={toggleSideNav} />
            <MainContent isOpen={isOpen}>
            </MainContent>
        </Container>
    );
}

export default SideNavComponent
