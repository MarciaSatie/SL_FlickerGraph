function XSheetToJson() {
    scene.beginUndoRedoAccum("XSheetToJson");

    // Dynamically generate the folder path
    var homeDirectory = System.getenv("USERPROFILE") || System.getenv("HOME");
    var folderPath = homeDirectory + "\\Desktop\\FlickerScript\\SL_FlickerGraph";
    
    var objList = [];

    // Get Path from Selected Node
    var selectedNodePath = selection.selectedNode(0);
    MessageLog.trace(selectedNodePath);

    var posX = getXValueList(selectedNodePath);
    var posY = getYValueList(selectedNodePath);

    for (var i in posX) {
        var obj = {};
        // Add values to the Object obj
        obj.id = parseInt(i) + 1;
        obj.posX = posX[i];
        obj.posY = posY[i];
        MessageLog.trace("at frame: " + i + " posX =" + posX[i] + " posY =" + posY[i]);
        objList.push(obj);
    }

    for (var i in objList) {
        MessageLog.trace("at frame: " + i + " Obj.X =" + objList[i].posX + " Obj.Y =" + objList[i].posY);
    }

    MessageLog.trace(scene.currentProjectPath());

    try {
        createExternalFile(objList, folderPath);
    } catch (e) {
        MessageLog.trace("Error creating file: " + e.message);
    }

    runGraph(folderPath);
    //if you want to open the folder after closing the graph, enable the line bellow.
    //open_log_folder_fs01(folderPath);

    scene.endUndoRedoAccum();
}

// Functions

// Return a list of values from position X
function getXValueList(selectedNodePath) {
    var xList = [];
    var sceneFrameNumber = frame.numberOf();

    for (var i = 1; i <= sceneFrameNumber; i++) {
        var num1 = node.getTextAttr(selectedNodePath, i, "POSITION.X");
        xList.push(num1);
    }

    return xList;
}

// Return a list of values from position Y
function getYValueList(selectedNodePath) {
    var yList = [];
    var sceneFrameNumber = frame.numberOf();

    for (var i = 1; i <= sceneFrameNumber; i++) {
        var num1 = node.getTextAttr(selectedNodePath, i, "POSITION.Y");
        yList.push(num1);
    }

    return yList;
}

// Function to create and write to a JSON file
function createExternalFile(textToAdd, path) {
    var first = "\\Z_FlickerValues";
    var logLocation = path;
    var second = ".json";
    var pathh = logLocation + first + second;
    var newFile = new File(pathh);

    try {
        newFile.open(FileAccess.WriteOnly);
        var jsonString = JSON.stringify(textToAdd, null, 2);
        newFile.write(jsonString);
        newFile.close();
        MessageLog.trace("File created successfully: " + pathh);
        return true;
    } catch (e) {
        MessageLog.trace("Error creating file: " + e.message);
        return false;
    }
}

// Open file location
function open_log_folder_fs01(path) {
    var userPath = path;
    Process.execute("explorer " + userPath);
}

// Run the Python script to generate the graph
function runGraph(path) {
    try {
        MessageLog.trace("Run runGraph");

        var pythonPath = "C:\\Python27\\python.exe";
        var scriptPath = path + "\\generateGraph.py";

        MessageLog.trace("Python Path: " + pythonPath);
        MessageLog.trace("Script Path: " + scriptPath);

        var command = pythonPath + " " + scriptPath;
        MessageLog.trace("Executing command: " + command);

        var process = new Process2(command);
        process.launch();
        process.waitForFinished();

        var stdOutput = process.readStdOut();
        var stdError = process.readStdErr();
        var exitCode = process.exitCode();

        MessageLog.trace("Process stdout: " + stdOutput);
        MessageLog.trace("Process stderr: " + stdError);
        MessageLog.trace("Process exit code: " + exitCode);

        if (exitCode !== 0) {
            MessageLog.trace("Process execution failed with exit code: " + exitCode);
        } else {
            MessageLog.trace("Process executed successfully.");
        }
    } catch (err) {
        MessageLog.trace("Process.execute ERROR: " + err);
    }
}
