import React, { useEffect, useRef, useState } from "react";
import PropTypes from "prop-types";
import { Chart } from "chart.js/auto";
import "./Severity.css";
import ChartActions from "../../../redux/actions/chartActions";
import { useDispatch, useSelector } from "react-redux";
import LoadingScreen from "../../ui/loader/Loader";
import RadioButton from "../../ui/buttons/RadioButton";
import { clearSeverityData } from "../../../redux/reducers/SeverityReducer";

const Severity = ({ id }) => {
  const [docType, setDocType] = useState("1");
  const [chartInstance, setChartInstance] = useState(null);
  const dispatch = useDispatch();
  const chartData = useSelector(
    (state) => state?.SeverityReducer?.SeverityData
  );
  const loading = useSelector((state) => state?.SeverityReducer?.isLoading);

  let labels = [];
  let table_Data = [];
  let data = [];

  if (chartData?.length > 0) {
    labels = chartData[1]?.labels[0];
    table_Data = chartData[0]?.table_data;

    data = {
      labels: labels,
      datasets: [
        {
          label: chartData[2]?.datasets[0]?.priority ? "High" : "",
          data: chartData[2]?.datasets[0]?.count.slice(),
          backgroundColor: "#4f81bd",
        },
        {
          label: chartData[2]?.datasets[1]?.priority ? "Medium" : "",
          data: chartData[2]?.datasets[1]?.count.slice(),
          backgroundColor: "#c0504d",
        },
        {
          label: chartData[2]?.datasets[2]?.priority ? "Low" : "",
          data: chartData[2]?.datasets[2]?.count.slice(),
          backgroundColor: "#9bbb59",
        },
      ],
    };
  }

  const chartRef = useRef(null);
  
  useEffect(() => {
    if (chartRef.current) {
      if (chartInstance) {
        chartInstance.destroy();
      }

      const ctx = chartRef.current.getContext("2d");
      const newChartInstance = new Chart(ctx, {
        type: "bar",
        data: data,
        options: {
          plugins: {},
          responsive: true,
          scales: {
            x: {
              stacked: true,
              grid: {
                display: false,
              },
            },
            y: {
              stacked: true,
            },
          },
        },
      });
      setChartInstance(newChartInstance);
    }
  
  }, [chartData]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const testCaseCategory = docType === "1" ? "UI" : "API";
        dispatch(ChartActions.SeverityChartAsync(id, testCaseCategory));
      } catch (error) {
        console.error("error", error);
      }
    };

    fetchData();
    return () => {
      dispatch(clearSeverityData())
    };
  }, [docType, id]);


  return (
    <>
      {loading && <LoadingScreen />}
      <div className="mainBox">
        <RadioButton docType={docType} setDocType={setDocType} />
        <div className="chart">
          <canvas ref={chartRef}></canvas>
        </div>
        <div className="sevTable">
        {table_Data?.length > 0 && (
          <table className="styledtable">
            <thead>
              <tr>
                <th rowSpan="2">Severity</th>
                <th colSpan="2">Bug</th>
              </tr>
              <tr>
                <th>Count</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              {table_Data
                ? table_Data?.map((row) => (
                    <tr key={row?.priority}>
                      <td>
                        {row?.priority === "normal"
                          ? "Medium"
                          : row?.priority.charAt(0).toUpperCase() +
                            row?.priority.slice(1)}
                      </td>
                      <td style={{ backgroundColor: "#fde9d9" }}>
                        {parseFloat(row.count)}
                      </td>
                      <td>{parseFloat(row?.percentage).toFixed(2)}</td>
                    </tr>
                  ))
                : ""}
            </tbody>
          </table>
        )}
        </div>
      </div>
    </>
  );
};

Severity.propTypes = {
  id: PropTypes.any.isRequired,
};

export default Severity;
