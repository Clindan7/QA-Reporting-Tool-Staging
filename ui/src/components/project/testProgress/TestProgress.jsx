import React, { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Chart from 'chart.js/auto';
import PropTypes from 'prop-types';
import "./TestProgress.css";
import DataInputModal from "../testProgress/DataInputModal";
import ChartActions from "../../../redux/actions/chartActions";
import LoadingScreen from "../../ui/loader/Loader";
import RadioButton from "../../ui/buttons/RadioButton";
import { clearTestProgressData } from "../../../redux/reducers/TestProgressReducer";

const TestProgress = ({ id }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [docType, setDocType] = useState("1");
  const [chartInstance, setChartInstance] = useState(null);
  const dispatch = useDispatch();
  const chartData = useSelector(
    (state) => state?.TestProgressReducer?.TestProgressData || {});
  const isLoading = useSelector((state) => state?.TestProgressReducer?.isLoading);
const [callAPI, setCallAPI] = useState(0);

  let testProgressData;

  if (chartData) {
    const labels = chartData?.dates || [];

    testProgressData = {
      labels: labels,
      datasets: [
        {
          label: 'Remaining TC',
          data: chartData?.categories?.remaingTcToExecute.slice() || [],
          type: 'line',
          borderColor: '#93cc56',
          borderWidth: 2
        },
        {
          label: 'TC Not Run',
          data: chartData?.categories?.tcNotRun.slice() || [],
          type: 'line',
          borderColor: '#6a597f',
          borderWidth: 2,
          borderDash: [5, 5]
        },
        {
          label: 'Total Bugs',
          data: chartData?.categories?.totalBugs.slice() || [],
          type: 'line',
          borderColor: '#00b0f0',
          borderWidth: 2,
          yAxisID: 'right-y-axis',
        },
        {
          label: 'Open Bugs',
          data: chartData?.categories?.openBugs.slice() || [],
          type: 'bar',
          backgroundColor: 'rgba(192,128,128)',
        },
      ],
    };
  }

  const chartRef = useRef(null);

  const closeModal = () => {
    setIsModalOpen(false);
    const count = callAPI +1;
    setCallAPI(count)
  };

  const handleClick = () => {
    setIsModalOpen(true);
  }

  useEffect(() => {
    if (chartRef.current) {
      if (chartInstance) {
        chartInstance.destroy();
      }
      const ctx = chartRef.current.getContext("2d");
      const newChartInstance = new Chart(ctx, {
        type: 'mixed',
        data: testProgressData,
        options: {
          plugins: {},
          responsive: true,
          elements: {
            point: {
              radius: .5
            }
          },
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
                display:false,
              }
            },
            y: {
              type: 'linear',
              display: true,
              position: 'left',
              title: {
                display: true,
                text: 'Testcase Count',
                position: 'top',
                font: {
                  size: 15
                }
              }
            },
            'right-y-axis': {
              position: 'right',
              type: 'linear',
              display: true,
              beginAtZero: true,
              title: {
                display: true,
                text: 'Number of bugs',
                position: 'top',
                font: {
                  size: 15
                },
              }
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
        dispatch(ChartActions.TestProgressChartAsync(id, testCaseCategory));
      } catch (error) {
        console.error("error", error);
      }
    };

    fetchData();
    return () => {
      dispatch(clearTestProgressData())
    };
  }, [docType, id, callAPI]);


  return (
    <>
      {isLoading && <LoadingScreen />}
      <div className="mainBox">
        <RadioButton docType={docType} setDocType={setDocType} />
        <div className="top-right-button"><button
          className="btn btn-enter1 me-md-2 "
          type="button"
          onClick={handleClick}>
          Enter Data
        </button></div>

        {isModalOpen ? (
          <DataInputModal isOpen={isModalOpen} handleClose={closeModal} projectid={id} docType={docType} />
        ) : null}
        <div className="chartProgress row">
          <canvas ref={chartRef} ></canvas>
        </div>
      </div>
    </>
  )
}

TestProgress.propTypes = {
  id: PropTypes.any.isRequired,
};

export default TestProgress
