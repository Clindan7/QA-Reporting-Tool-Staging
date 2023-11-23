import {instance} from "./Instance";

async function FeatureTable(id,testCaseCategory){
    try{
        const res =await instance.get(`report/featureWiseSummaryReport/${id}?testCaseCategory=${testCaseCategory}`);
        return res;
    }catch(error){
        console.log(error);
    }
}

export const TableService ={
    FeatureTable
}