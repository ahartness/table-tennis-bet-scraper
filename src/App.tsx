// Package Imports
import { useState, useEffect } from 'react'
import { Bar } from 'react-chartjs-2'
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend, ChartData } from 'chart.js';

// Custom Component Imports
import ChartDataLabels from 'chartjs-plugin-datalabels'
import SideNavComponent from './components/sidenav';

// Data Imports
import h2h_data from '../data/all_h2h_plays.json'
import home_data from '../data/all_home_plays.json'
import away_data from '../data/all_away_plays.json'
import best_data from '../data/table-tennis-best-plays.json'

// Utility Imports
import { parseDate } from './utils/dateconversion';
import { point_totals, game_totals } from './utils/staticvars';

// CSS Styling Imports
import './App.css'
import TennisBoxScore from './components/gametable/TennisBoxScore';

const calculateCounts = (data1: string[], data2: string[], displayCount: number) => {
    const counts1 = { H: 0, A: 0, S: 0 };
    const counts2 = { H: 0, A: 0, S: 0 };
    [...data1].reverse().slice(-displayCount).forEach(item => {
        if (item === "H") counts1.H++;
        else if (item === "A") counts1.A++;
        else if (item === "S") counts1.S++;
    });
    [...data2].reverse().slice(-displayCount).forEach(item => {
        if (item === "H") counts2.H++;
        else if (item === "A") counts2.A++;
        else if (item === "S") counts2.S++;
    });
    return {first: counts1, second: counts2};
}

const calculatePercentages = (counts: { H: number, A: number, S: number }, displayCount: number) => {
    return {
        H: ((counts.H / displayCount) * 100).toFixed(2),
        A: ((counts.A / displayCount) * 100).toFixed(2),
        S: ((counts.S / displayCount) * 100).toFixed(2)
    };
};

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend, ChartDataLabels);
function App() {
    const [displayCount, setDisplayCount] = useState(5)
    const [displayTarget, setDisplayTarget] = useState(74.5)
    // const [selectedDataset, setSelectedDataset] = useState(h2h_data.findIndex((data: any) => parseDate(data["date"]) > new Date(new Date().getTime() - 25 * 60 * 1000)))
    const [selectedDataset, setSelectedDataset] = useState(0)
    const [datasetType, setDatasetType] = useState("h2h_datasets")
    const [subDatasetType, setSubDatasetType] = useState("scores_dataset")
    const [allData, setAllData] = useState([])
    const [options, setOptions] = useState({})
    const [hitRate, setHitRate] = useState(0)
    const [hitRateDivisor, setHitRateDivisor] = useState(1)
    const [dataSelection, setDataSelection] = useState("all")
    const [jsonData, setJsonData] = useState(h2h_data)
    const [thresholdOptions, setThresholdOptions] = useState(point_totals)
    const [dataOptions, setDataOptions] = useState("Points")
    const [hitRateColor, setHitRateColor] = useState("red")
    const [appTitle, setAppTitle] = useState("All TT Plays")
    const [counts, setCounts] = useState({first: { H: 0, A: 0, S: 0 }, second: { H: 0, A: 0, S: 0 }})
    const [percentages, setPercentages] = useState({first: { H: "0.00", A: "0.00", S: "0.00" }, second: { H: "0.00", A: "0.00", S: "0.00" }});
    const [historyTableData, setHistoryTableData] = useState({ dates: [], scoreHistory: [], homePlayer: "", awayPlayer: "" })

    useEffect(() => {
        if (dataOptions === "Points") {
            setThresholdOptions(point_totals)
        } else if (dataOptions === "Games") {
            setThresholdOptions(game_totals)
        } else if (dataOptions === "1st Set") {
            setThresholdOptions([2.5, 3.5])
        }
    }, [dataOptions])

    useEffect(() => {
        if (datasetType == 'h2h_datasets') {
            setJsonData(h2h_data)
            setHistoryTableData({ 
                dates: h2h_data[selectedDataset]["h2h_datasets"]["dates"], 
                scoreHistory: h2h_data[selectedDataset]["h2h_datasets"]["score_history"],
                homePlayer: h2h_data[selectedDataset]["home_player"],
                awayPlayer: h2h_data[selectedDataset]["away_player"]
            })
        }
        if (datasetType == 'home_datasets') {
            setJsonData(home_data)
            setHistoryTableData({ 
                dates: home_data[selectedDataset]["home_datasets"]["dates"], 
                scoreHistory: home_data[selectedDataset]["home_datasets"]["score_history"], 
                homePlayer: h2h_data[selectedDataset]["home_player"],
                awayPlayer: "Opponent"
            })
        }
        if (datasetType == 'away_datasets') {
            setJsonData(away_data)
            setHistoryTableData({ 
                dates: away_data[selectedDataset]["away_datasets"]["dates"], 
                scoreHistory: away_data[selectedDataset]["away_datasets"]["score_history"],
                homePlayer: "Opponent",
                awayPlayer: h2h_data[selectedDataset]["away_player"]
            })
        }

        if (dataOptions == "Points") {
            setSubDatasetType("scores_dataset")
            setDisplayTarget(74.5)
        } else if (dataOptions == "Games") {
            setSubDatasetType("games_dataset")
            setDisplayTarget(3.5)
        } else {
            setSubDatasetType("1st_dataset")
            setDisplayTarget(2.5)
        }

    }, [thresholdOptions, datasetType, selectedDataset])

    useEffect(() => {
        setJsonData(h2h_data)
        setHistoryTableData({ 
            dates: h2h_data[selectedDataset]["h2h_datasets"]["dates"], 
            scoreHistory: h2h_data[selectedDataset]["h2h_datasets"]["score_history"],
            homePlayer: h2h_data[selectedDataset]["home_player"],
            awayPlayer: h2h_data[selectedDataset]["away_player"]
        })
    }, [])

    useEffect(() => {

    }, [displayCount])

    useEffect(() => {
        //setSelectedDataset(0)
        setAppTitle(dataSelection == 'all' ? "All Table Tennis Plays" : "Best Table Tennis Plays")
    }, [dataSelection])

    useEffect(() => {
        if (jsonData) {
            let reversedSet = [...jsonData[selectedDataset][datasetType][subDatasetType]]
            let reversedLabels = [...jsonData[selectedDataset][datasetType]["dates"]].splice(0, displayCount)
            // Calculate totals for each bar
            const totals = reversedSet[0].data.map((_: any, i: any) =>
                reversedSet.reduce((sum: number, dataset: any) => sum + dataset.data[i], 0)
            );

            // Generate colors dynamically for each section
            const getShadedColor = (baseColor: any, shadeFactor: any) => {
                const [r, g, b] = baseColor.match(/\d+/g).map(Number);
                return `rgba(${Math.min(r + shadeFactor, 255)}, ${Math.min(g + shadeFactor, 255)}, ${Math.min(b + shadeFactor, 255)}, 0.8)`;
            };

            const baseColors = totals.map(total => {
                if (total < displayTarget) return [255, 99, 132]; // Base color for low totals
                return [60, 179, 113]; // Base color for high totals
            });

            const datasetsWithColors = reversedSet.map((dataset: any, datasetIndex: number) => ({
                ...dataset,
                backgroundColor: dataset.data.map((_: any, barIndex: number) =>
                    getShadedColor(`rgb(${baseColors[barIndex].join(",")})`, datasetIndex * 50)
                ),
                borderColor: dataset.data.map((_: any, barIndex: number) =>
                    getShadedColor(`rgb(${baseColors[barIndex].join(",")})`, datasetIndex * 50).replace('0.8', '1')
                ),
                borderWidth: 1,
            }));

            setAllData({
                labels: reversedLabels,
                datasets: datasetsWithColors
            })

            setOptions({
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    datalabels: {
                        display: (ctx: any) => ctx.datasetIndex === ctx.chart.data.datasets.length - 1 && ctx.chart.data.labels.length < 20, // Display only for the last dataset
                        anchor: 'end',
                        align: 'start',
                        formatter: (value: any, ctx: { dataIndex: number; chart: { data: ChartData } }) => {
                            const index = ctx.dataIndex;
                            const total = ctx.chart.data.datasets.reduce(
                                (sum: number, dataset: any) => sum + dataset.data[index],
                                0
                            );
                            return total;
                        },
                        font: {
                            size: 15,
                        },
                        color: '#000', // Black color for the totals
                    },
                    thresholdLine: {
                        value: displayTarget,
                        color: 'white',
                        width: 2,
                        dash: [5, 5]
                    },
                    tooltip: {
                        enabled: true,
                        displayColors: false,
                        callbacks: {
                            // Customize the tooltip title
                            title: (tooltipItems: any) => {
                                const { label } = tooltipItems[0]; // Get the label for the bar
                                return `${label}`;
                            },
                            // Tooltip body: Display aggregated information
                            label: (tooltipItems: any) => {
                                const total = datasetsWithColors.reduce(
                                    (sum, dataset) => sum + dataset.data[tooltipItems.dataIndex],
                                    0
                                );
                                return `Total ${dataOptions}: ${total}`;
                            },
                            // Optional footer: Display breakdown of each dataset
                            footer: (tooltipItems: any) => {
                                const index = tooltipItems[0].dataIndex; // Get bar index
                                const breakdown = datasetsWithColors.map(
                                    (dataset) => `${Array.isArray(dataset.label) ? dataset.label[index] : dataset.label}: ${dataset.data[index]}`
                                );
                                return breakdown.join('\n');
                            },
                        },
                        bodyFont: {
                            size: 14
                        },
                        titleFont: {
                            size: 16
                        }
                    }
                },
                scales: {
                    x: {
                        stacked: (dataOptions === "Points" || dataOptions === "Games") ? true : false,
                        reverse: true,
                        ticks: {
                            callback: (index: any) => {
                                const fullLabel = reversedLabels[index]
                                return fullLabel.substring(5, 10)
                            },
                            font: {
                                size: 14,
                            },
                            maxRotations: 45,
                            minRotations: 0,
                        }
                    },
                    y: {
                        stacked: (dataOptions === "Points" || dataOptions === "Games") ? true : false,
                        ticks: {
                            font: {
                                size: 12
                            },
                        },
                    }
                }
            })

            const tempTotals = [...totals]
            const stacksAboveThreshold = tempTotals.splice(0, displayCount).filter((total: number) => total > displayTarget).length
            const stackDivisor = (displayCount > totals.length) ? totals.length : displayCount

            setHitRate(stacksAboveThreshold)
            setHitRateDivisor(stackDivisor)
            if (stacksAboveThreshold / stackDivisor >= .7 || stacksAboveThreshold / stackDivisor <= .25) {
                setHitRateColor("green")
            } else {
                setHitRateColor("red")
            }

            const countData1 = jsonData[selectedDataset][datasetType]["1st_and_2nd_sets"]
            const countData2 = jsonData[selectedDataset][datasetType]["2nd_and_3rd_sets"]
            const newCounts = calculateCounts(countData1, countData2, displayCount)
            setCounts(newCounts);
            const newPercentages1 = calculatePercentages(newCounts.first, displayCount);
            const newPercentages2 = calculatePercentages(newCounts.second, displayCount);
            setPercentages({first: newPercentages1, second: newPercentages2});
        }
    }, [displayTarget, displayCount, selectedDataset, subDatasetType, jsonData])




    const thresholdLinePlugin = {
        id: 'thresholdLine',
        beforeDraw: (chart: any) => {
            const { ctx, chartArea, scales } = chart;
            const { value, color, width, dash } = chart.options.plugins.thresholdLine || {};
            if (value !== undefined && scales.y) {
                const yValue = scales.y.getPixelForValue(value);

                ctx.save();
                ctx.beginPath();
                ctx.setLineDash(dash || []); // Dashed line pattern
                ctx.lineWidth = width || 1;
                ctx.strokeStyle = color || 'black';
                ctx.moveTo(chartArea.left, yValue);
                ctx.lineTo(chartArea.right, yValue);
                ctx.stroke();
                ctx.restore();
            }
        }
    }

    ChartJS.register(thresholdLinePlugin)

    if (!jsonData || jsonData.length == 0 || allData.length == 0) {
        return <div>Loading...</div>
    } else {
        return (
            <>
                <SideNavComponent onDataSelectionChange={setSelectedDataset} jsonData={jsonData} bestPlays={best_data} />
                <h2 style={{ textAlign: 'center', marginBottom: '0px' }}>{appTitle} Visualization</h2>

                {/* Dropdown for dataset selection
                <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px', margin: '10px 10px' }}>
                    <select
                        value={selectedDataset}
                        onChange={(e) => setSelectedDataset(Number(e.target.value))}
                        style={{
                            padding: '10px',
                            fontSize: '14px',
                            borderRadius: '5px',
                            border: '1px solid #28a745',
                            cursor: 'pointer',
                            width: '95%',
                            maxWidth: '600px'
                        }}
                    >
                        {Object.keys(jsonData).map((datasetKey: any) => {
                            if (parseDate(jsonData[datasetKey]["date"]) > new Date(new Date().getTime() - 25 * 60 * 1000)) {
                                return (<option key={datasetKey} value={datasetKey}>
                                    {jsonData[datasetKey]["date"].substring(5, 10)} {jsonData[datasetKey]["date"].substring(11, 20)} - {jsonData[datasetKey]["home_player"].substring(0, 12)} vs. {jsonData[datasetKey]["away_player"].substring(0, 12)}
                                </option>)
                            }
                        })}
                    </select>
                </div > */}
                <hr />
                <div style={{ marginBottom: '5px', display: "flex" }}>
                    <div style={{ marginLeft: '10px' }}>
                        <div>{h2h_data[selectedDataset]["home_player"]} vs {h2h_data[selectedDataset]["away_player"]}</div>
                        <div>{h2h_data[selectedDataset]["date"]}</div>
                        <div>Confidence: {(h2h_data[selectedDataset]["mean"]).toFixed(2)}±{(h2h_data[selectedDataset]["confidence_interval"]).toFixed(2)} &nbsp;
                            <span>[{(h2h_data[selectedDataset]["mean"] - h2h_data[selectedDataset]["confidence_interval"]).toFixed(2)} - {(h2h_data[selectedDataset]["mean"] + h2h_data[selectedDataset]["confidence_interval"]).toFixed(2)}]</span></div>

                    </div>
                    <div style={{ border: '3px solid #000', marginRight: '10px', padding: "2px", textAlign: "center", position: "absolute", right: 0, backgroundColor: hitRateColor }}>
                        <div>Hit Rate: </div>{((hitRate / hitRateDivisor) * 100).toFixed(2)}%
                    </div>
                </div>

                <hr />


                <div style={{ justifySelf: 'center', width: '100%', height: '300px', maxWidth: '800px', border: '.5px solid #fff', borderRadius: '5px', backgroundColor: '#242424' }}>
                    <Bar data={allData} options={options} />
                </div>
                <div style={{ marginTop: '20px', display: 'flex', overflowX: 'auto', justifyContent: 'center', gap: '10px', paddingLeft: '10px' }}>
                    {[5, 10, 15, 20, 25, 30].map((count) => (
                        <button
                            key={count}
                            onClick={() => setDisplayCount(count)}
                            style={{
                                padding: '10px 15px',
                                fontSize: '14px',
                                backgroundColor: displayCount === count ? '#28a745' : '#242424',
                                color: displayCount === count ? '#000' : '#fff',
                                border: '1px solid #fff',
                                borderRadius: '5px',
                                cursor: 'pointer',
                                transition: 'background-color 0.3s, color 0.3s', // Smooth transition for both background and text color
                            }}
                        // disabled={jsonData[selectedDataset][datasetType][subDatasetType][0]["data"].length < (count - 5)}
                        >
                            Last {count}{' '}
                            {/**jsonData[selectedDataset]["dataset_array"][0]["data"].length >= displayCount ?
                                `${(
                                    ([...jsonData[selectedDataset]["dataset_array"][0]["data"]]
                                        .slice(-count)
                                        .map((v, i) => v + [...jsonData[selectedDataset]["dataset_array"][1]["data"]].reverse().slice(-count)[i])
                                        .filter((v) => v > displayTarget).length / count) * 100).toFixed(2)}%` : '(N/A)'**/}
                        </button>
                    ))}
                </div>

                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px', gap: '10px' }}>
                    {["Points", "Games", "1st Set"].map((type) => (
                        <button
                            key={type}
                            onClick={() => setDataOptions(type)}
                            style={{
                                padding: '5px 5px',
                                fontSize: '16px',
                                backgroundColor: dataOptions == type ? '#28a745' : '#242424',
                                color: dataOptions == type ? '#000' : '#fff',
                                border: '1px solid #fff',
                                borderRadius: '5px',
                                cursor: 'pointer',
                                transition: 'background-color 0.3s, color 0.3s'

                            }}
                        >
                            {type}
                        </button>
                    ))}
                </div><div style={{ padding: '5px 0', width: '100%', overflowX: "auto", marginTop: '5px', display: 'flex', justifyContent: 'center', gap: '5px' }}>
                    {thresholdOptions.map((count) => (
                        <button
                            key={count}
                            onClick={() => setDisplayTarget(count)}
                            style={{
                                padding: '5px 5px',
                                fontSize: '14px',
                                backgroundColor: displayTarget === count ? '#28a745' : '#242424',
                                color: displayTarget === count ? '#000' : '#fff',
                                border: '1px solid #fff',
                                borderRadius: '5px',
                                cursor: 'pointer',
                                transition: 'background-color 0.3s, color 0.3s', // Smooth transition for both background and text color
                            }}
                        >
                            {count}
                        </button>
                    ))}
                </div>
                <div style={{ padding: '10px 0', width: '100%', marginTop: "auto", display: 'flex', justifyContent: 'center', gap: '5px' }}>
                    {["Head to Head", jsonData[selectedDataset]["home_player"], jsonData[selectedDataset]["away_player"]].map((player) => (
                        <button
                            key={player}
                            onClick={() => setDatasetType(player == "Head to Head" ? "h2h_datasets" : player == jsonData[selectedDataset]["home_player"] ? "home_datasets" : "away_datasets")}
                            style={{
                                padding: '5px 5px',
                                fontSize: '14px',
                                backgroundColor: datasetType == (player == "Head to Head" ? "h2h_datasets" : player == jsonData[selectedDataset]["home_player"] ? "home_datasets" : "away_datasets") ? '#28a745' : '#242424',
                                color: datasetType == (player == "Head to Head" ? "h2h_datasets" : player == jsonData[selectedDataset]["home_player"] ? "home_datasets" : "away_datasets") ? '#000' : '#fff',
                                transition: 'background-color 0.3s, color 0.3s',
                                borderRadius: '5px',
                                border: '1px solid #fff'
                            }}
                        >
                            {player}
                        </button>
                    ))}
                </div>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '5px', marginTop: '5px', flexDirection: 'column' }}>
                    <h3 style={{ alignSelf: 'center', margin: '2px 2px'}}>Win Counts</h3>
                    <div style={{ justifyContent: 'space-around', display: 'flex'}}>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px'}} >
                            <div style={{ borderBottom: '1px solid #fff'}}>{jsonData[selectedDataset]["home_player"]}</div>
                            <div style={{ display: 'flex', justifyContent: 'space-evenly', gap: '5px', flexDirection: 'row' }}>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>H2H</u></div>
                                    <div>
                                        {[...h2h_data[selectedDataset]["h2h_datasets"]["games_dataset"][0]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item == 3
                                        }).length}
                                    </div>
                                </div>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', borderLeft: '1px solid #fff', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>Last {displayCount}</u></div>
                                    <div>
                                        {[...home_data[selectedDataset]["home_datasets"]["games_dataset"][0]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item == 3
                                        }).length}
                                    </div> 
                                </div>
                            </div>
                        </div>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px'}} >
                            <div style={{ borderBottom: '1px solid #fff'}}>{jsonData[selectedDataset]["away_player"]}</div>
                            <div style={{ display: 'flex', justifyContent: 'space-around', gap: '5px', flexDirection: 'row' }}>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>H2H</u></div>
                                    <div>
                                        {[...h2h_data[selectedDataset]["h2h_datasets"]["games_dataset"][1]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item == 3
                                        }).length}
                                    </div>
                                </div>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', borderLeft: '1px solid #fff', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>Last {displayCount}</u></div>
                                    <div>
                                        {[...away_data[selectedDataset]["away_datasets"]["games_dataset"][1]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item == 3
                                        }).length}
                                    </div> 
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '5px', marginTop: '5px', flexDirection: 'column' }}>
                    <h3 style={{ alignSelf: 'center', margin: '2px 2px'}}>1st Game Spread</h3>
                    <div style={{ justifyContent: 'space-around', display: 'flex'}}>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px'}} >
                            <div style={{ borderBottom: '1px solid #fff'}}>{jsonData[selectedDataset]["home_player"]} -2.5</div>
                            <div style={{ display: 'flex', justifyContent: 'space-evenly', gap: '5px', flexDirection: 'row' }}>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>H2H</u></div>
                                    <div>
                                        {[...h2h_data[selectedDataset]["h2h_datasets"]["1st_dataset"][0]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item > (h2h_data[selectedDataset]["h2h_datasets"]["1st_dataset"][1]["data"][index] + 2)
                                        }).length}
                                    </div>
                                </div>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', borderLeft: '1px solid #fff', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>Last {displayCount}</u></div>
                                    <div>
                                        {[...home_data[selectedDataset]["home_datasets"]["1st_dataset"][0]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item > (home_data[selectedDataset]["home_datasets"]["1st_dataset"][1]["data"][index] + 2)
                                        }).length}
                                    </div> 
                                </div>
                            </div>
                        </div>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px'}} >
                            <div style={{ borderBottom: '1px solid #fff'}}>{jsonData[selectedDataset]["away_player"]} -2.5</div>
                            <div style={{ display: 'flex', justifyContent: 'space-around', gap: '5px', flexDirection: 'row' }}>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>H2H</u></div>
                                    <div>
                                        {[...h2h_data[selectedDataset]["h2h_datasets"]["1st_dataset"][1]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item > (h2h_data[selectedDataset]["h2h_datasets"]["1st_dataset"][0]["data"][index] + 2)
                                        }).length}
                                    </div>
                                </div>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', borderLeft: '1px solid #fff', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>Last {displayCount}</u></div>
                                    <div>
                                        {[...away_data[selectedDataset]["away_datasets"]["1st_dataset"][1]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item > (away_data[selectedDataset]["away_datasets"]["1st_dataset"][0]["data"][index] + 2)
                                        }).length}
                                    </div> 
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '5px', marginTop: '5px', flexDirection: 'column' }}>
                    <h3 style={{ alignSelf: 'center', margin: '2px 2px'}}>1st Game Winner</h3>
                    <div style={{ justifyContent: 'space-around', display: 'flex'}}>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px'}} >
                            <div style={{ borderBottom: '1px solid #fff'}}>{jsonData[selectedDataset]["home_player"]}</div>
                            <div style={{ display: 'flex', justifyContent: 'space-evenly', gap: '5px', flexDirection: 'row' }}>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>H2H</u></div>
                                    <div>
                                        {[...h2h_data[selectedDataset]["h2h_datasets"]["1st_dataset"][0]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item > (h2h_data[selectedDataset]["h2h_datasets"]["1st_dataset"][1]["data"][index])
                                        }).length}
                                    </div>
                                </div>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', borderLeft: '1px solid #fff', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>Last {displayCount}</u></div>
                                    <div>
                                        {[...home_data[selectedDataset]["home_datasets"]["1st_dataset"][0]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item > (home_data[selectedDataset]["home_datasets"]["1st_dataset"][1]["data"][index])
                                        }).length}
                                    </div> 
                                </div>
                            </div>
                        </div>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px'}} >
                            <div style={{ borderBottom: '1px solid #fff'}}>{jsonData[selectedDataset]["away_player"]}</div>
                            <div style={{ display: 'flex', justifyContent: 'space-around', gap: '5px', flexDirection: 'row' }}>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>H2H</u></div>
                                    <div>
                                        {[...h2h_data[selectedDataset]["h2h_datasets"]["1st_dataset"][1]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item > (h2h_data[selectedDataset]["h2h_datasets"]["1st_dataset"][0]["data"][index])
                                        }).length}
                                    </div>
                                </div>
                                <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', borderLeft: '1px solid #fff', textAlign: 'center', flex: 1, margin: '0 3px'}}>
                                    <div><u>Last {displayCount}</u></div>
                                    <div>
                                        {[...away_data[selectedDataset]["away_datasets"]["1st_dataset"][1]["data"]].splice(0, displayCount).filter((item, index) => {
                                            return item > (away_data[selectedDataset]["away_datasets"]["1st_dataset"][0]["data"][index])
                                        }).length}
                                    </div> 
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {/* Title and table to show counts */}
                <div style={{ display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center', marginTop: '5px' }}>
                    <h4 style={{ margin: '5px'}}>Sets 1 & 2</h4>
                    <div style={{ display: 'flex', justifyContent: 'space-around', width: '95%', backgroundColor: '#242424', color: '#fff', borderRadius: '5px', overflow: 'hidden', padding: '2px' }}>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px' }}>
                            <div>{jsonData[selectedDataset]["home_player"].charAt(0)}. {jsonData[selectedDataset]["home_player"].split(" ")[1]}</div>
                            <div>{counts.first.H} - {percentages.first.H}%</div>
                        </div>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px',border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px' }}>
                            <div>{jsonData[selectedDataset]["away_player"].charAt(0)}. {jsonData[selectedDataset]["away_player"].split(" ")[1]}</div>
                            <div>{counts.first.A} - {percentages.first.A}%</div>
                        </div>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px',border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px' }}>
                            <div>Split Games</div>
                            <div>{counts.first.S} - {percentages.first.S}%</div>
                        </div>
                    </div>
                </div>
                {/* Title and table to show counts */}
                <div style={{ maxWidth: '100%', display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center' }}>
                    <h4 style={{ margin: '5px'}}>Sets 2 & 3</h4>
                    <div style={{ display: 'flex', justifyContent: 'space-around', width: '95%', backgroundColor: '#242424', color: '#fff', borderRadius: '5px', overflow: 'hidden', padding: '2px' }}>
                        <div style={{ whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px', border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px' }}>
                            <div>{jsonData[selectedDataset]["home_player"].charAt(0)}. {jsonData[selectedDataset]["home_player"].split(" ")[1]}</div>
                            <div>{counts.second.H} - {percentages.second.H}%</div>
                        </div>
                        <div style={{overflowX: 'hidden', whiteSpace: 'nowrap',backgroundColor: '#242424', padding: '2px',border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px' }}>
                            <div>{jsonData[selectedDataset]["away_player"].charAt(0)}. {jsonData[selectedDataset]["away_player"].split(" ")[1]}</div>
                            <div>{counts.second.A} - {percentages.second.A}%</div>
                        </div>
                        <div style={{whiteSpace: 'nowrap', backgroundColor: '#242424', padding: '2px',border: '1px solid #fff', borderRadius: '5px', textAlign: 'center', flex: 1, margin: '0 3px' }}>
                            <div>Split Games</div>
                            <div>{counts.second.S} - {percentages.second.S}%</div>
                        </div>
                    </div>
                </div>
                <div>
                    <h4 style={{ justifySelf: 'center', margin: '2px 2px', marginTop: '10px' }}>History</h4>
                    <TennisBoxScore Dates={historyTableData.dates} scoreHistory={historyTableData.scoreHistory} HomePlayer={historyTableData.homePlayer} AwayPlayer={historyTableData.awayPlayer}/>
                    
                </div>
            </>
        )
    }


}

export default App
