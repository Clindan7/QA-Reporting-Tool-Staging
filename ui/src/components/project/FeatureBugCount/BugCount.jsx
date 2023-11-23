import React, { useEffect, useRef, useState, useCallback } from "react";
import PropTypes from "prop-types";
import { Chart } from 'chart.js/auto';
import "./BugCount.css"
import { toast } from "react-toastify";
import { chartService } from "../../../redux/services/ChartService";
import LoadingScreen from "../../ui/loader/Loader";
import RadioButton from "../../ui/buttons/RadioButton";

const BugCount = ({ id }) => {
  const [docType, setDocType] = useState("1");
  const [chartInstance, setChartInstance] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  let keysArray = [];
  let valuesArray = [];
  let bugCountData = {};
  
  const setBugCountData = useCallback(async () => {
    bugCountData = {
      labels: keysArray,
      datasets: [{
        label: 'Feature Wise Bug Count',
        data: valuesArray,
        backgroundColor: [
          'rgba(254,172,172)'
        ],
        borderColor: [
          'rgb(214,165,165)'
        ],
        borderWidth: 1
      }]
    };
  }, [keysArray, valuesArray])

  const chartRef = useRef(null);
  const drawChart = () =>{
    if (chartRef.current) {
      if (chartInstance) {
        chartInstance.destroy();
      }
      const ctx = chartRef.current.getContext('2d');
      const newChartInstance = new Chart(ctx, {
        type: 'bar',
        data: bugCountData,
        options: {
          scales: {
            x: {
              stacked: true,
              ticks:{
                font:{
                  size:9
                },
                display: true,
                maxRotation: 90, 
                minRotation:90,
                autoSkip: false,
              },
              grid:{
                display:false
              },
            },
            y: {
              beginAtZero: true
            }
          }
        }
      });
      setChartInstance(newChartInstance);
    }
  }
  const fetchData = async (id, docType) => {
    try {
      setIsLoading(true);
      const response = await chartService.getBugcountReport(id, docType);
      if (response?.status === 200) {
        const newData = response?.data?.feature_wise_bug_count;
        keysArray = Object.keys(newData);
        valuesArray = Object.values(newData);
        setBugCountData();
        drawChart()
      } else {
        toast.error("Failed to get Feature wise bug count!")
        console.error("API request failed:", response);
      }
    } catch (error) {
      toast.error("An error occurred while fetching Feature wise bug count");
      console.error("An error occurred while fetching data:", error);
    }
    finally{
      setIsLoading(false);
    }
  }

  useEffect(() => {
    fetchData(id, docType);
  }, [docType, id]);

  return (
    <>
    {isLoading && <LoadingScreen />}
    <div className='mainBox'>
    <RadioButton docType={docType} setDocType={setDocType} />
      <div className="chart">
        <canvas ref={chartRef}></canvas>
      </div>
    </div>
    </>
  );
}

BugCount.propTypes = {
  id: PropTypes.any.isRequired,
};

export default BugCount;

