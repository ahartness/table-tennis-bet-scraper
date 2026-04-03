import React from "react";
import styled from "styled-components";

const TableContainer = styled.div`
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 97%;
  overflow-x: auto;

  @media (max-width: 768px) {
    padding: 5px;
  }
`;

const ScoreTable = styled.table`
  width: 100%;
  border-collapse: collapse;

  th,
  td {
    text-align: center;
    padding: 10px;
    border: 1px solid #ddd;
    font-size: 14px;
  }

  th {
    background-color: #4caf50;
    color: white;
  }

  td {
    background-color: #242424;
  }

  @media (max-width: 768px) {
    th,
    td {
      padding: 5px;
      font-size: 12px;
    }
  }
`;

interface ScoreHistory {
    home: number[][];
    away: number[][];
  }

const TennisScoreHistory: React.FC<{ scoreHistory: ScoreHistory, HomePlayer: string, AwayPlayer: string, Dates: string[] }> = ({ scoreHistory, HomePlayer, AwayPlayer, Dates }) => {
    const { home, away } = scoreHistory;

    if(home.length === 0) { 
        return <div>No games played yet</div>;
    }

    const maxSets = 5;

    const padScores = (scores: number[]): (number | string)[] => {
        return [...scores, ...Array(maxSets > scores.length ? maxSets - scores.length : 0).fill('-')];
      };
  
    return (
      <TableContainer>
        {home.map((game, gameIndex) => (
          <div key={gameIndex}>
            {/* <h3>Game {gameIndex + 1}</h3> */}
            <ScoreTable>
              <thead>
                <tr>
                  <th>{Dates[gameIndex]}</th>
                  {Array.from({ length: maxSets }, (_, index) => (
                  <th key={index}>Set {index + 1}</th>
                ))}
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{HomePlayer}</td>
                  {padScores(home[gameIndex]).map((score, index) => (
                  <td key={index}>{score}</td>
                ))}
                </tr>
                <tr>
                  <td>{AwayPlayer}</td>
                  {padScores(away[gameIndex]).map((score, index) => (
                  <td key={index}>{score}</td>
                ))}
                </tr>
              </tbody>
            </ScoreTable>
          </div>
        ))}
      </TableContainer>
    );
  };
  
  export default TennisScoreHistory;
