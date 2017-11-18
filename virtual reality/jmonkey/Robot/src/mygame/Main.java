package mygame;

import com.jme3.app.SimpleApplication;
import com.jme3.material.Material;
import com.jme3.math.ColorRGBA;
import com.jme3.math.Vector3f;
import com.jme3.renderer.RenderManager;
import com.jme3.scene.Geometry;
import com.jme3.scene.Node;
import com.jme3.scene.shape.Box;
import java.util.HashMap;
import java.util.Map;

/**
 * This is the Main Class of your Game. You should only do initialization here.
 * Move your Logic into AppStates or Controls
 * @author normenhansen
 */
public class Main extends SimpleApplication {
    private Boolean liftLeft;
    private Integer framesLeft;
    
    public static void main(String[] args) {
        Main app = new Main();
        app.start();
        
    }

    @Override
    public void simpleInitApp() {
        this.liftLeft = Boolean.FALSE;
        this.framesLeft = 30;
        Map<String, Material> materials = new HashMap<>(); 
        materials.put("body", new Material(assetManager, "Common/MatDefs/Misc/Unshaded.j3md")); //BODY
        materials.put("head", new Material(assetManager, "Common/MatDefs/Misc/Unshaded.j3md")); //HEAD
        materials.put("abdomen", new Material(assetManager, "Common/MatDefs/Misc/Unshaded.j3md")); // ABDOMEN
        materials.put("upperArm", new Material(assetManager, "Common/MatDefs/Misc/Unshaded.j3md")); //UPPER ARMS
        materials.put("lowerArm", new Material(assetManager, "Common/MatDefs/Misc/Unshaded.j3md")); //LOWER ARMS
        materials.put("upperLeg", new Material(assetManager, "Common/MatDefs/Misc/Unshaded.j3md")); //UPPER LEGS
        materials.put("lowerLeg", new Material(assetManager, "Common/MatDefs/Misc/Unshaded.j3md")); //LOWER LEGS
        
        materials.get("body").setColor("Color", ColorRGBA.Blue);
        materials.get("head").setColor("Color", ColorRGBA.Red);
        materials.get("abdomen").setColor("Color", ColorRGBA.Cyan);
        materials.get("upperArm").setColor("Color", ColorRGBA.Yellow);
        materials.get("lowerArm").setColor("Color", ColorRGBA.Orange);
        materials.get("upperLeg").setColor("Color", ColorRGBA.Brown);
        materials.get("lowerLeg").setColor("Color", ColorRGBA.White);
        
        
        Box body = new Box(0.9f,0.6f,0.3f);
        Geometry bodyGeometry = new Geometry("Box", body);
        bodyGeometry.setLocalTranslation(new Vector3f(0,0,0));
        
        Box head = new Box(body.xExtent / 3, body.yExtent / 2, body.zExtent * 0.9f);
        Geometry headGeometry = new Geometry("Box", head);
        headGeometry.setLocalTranslation(new Vector3f(0, 0, 0));
        
        Box abdomen = new Box(body.xExtent * 0.7f, body.yExtent / 2, body.zExtent * 0.9f);
        Geometry abdomenGeometry = new Geometry("abdomen", abdomen);
        abdomenGeometry.setLocalTranslation(new Vector3f(
                0, 
                - abdomen.yExtent, 
                0));
             
        Box rightUpperArm = new Box(body.xExtent / 6, body.yExtent * 0.9f, body.zExtent * 0.75f);
        Geometry rightUpperArmGeometry = new Geometry("Box", rightUpperArm);
        rightUpperArmGeometry.setLocalTranslation(new Vector3f(
                0,
                0,
                0));
        
        Box rightLowerArm = new Box(body.xExtent / 6, body.yExtent, body.zExtent * 0.75f);
        Geometry rightLowerArmGeometry = new Geometry("Box", rightLowerArm);
        rightLowerArmGeometry.setLocalTranslation(new Vector3f(
                0,
                0,
                0));
        
        Box leftUpperArm = new Box(body.xExtent / 6, body.yExtent * 0.9f, body.zExtent * 0.75f);
        Geometry leftUpperArmGeometry = new Geometry("Box", leftUpperArm);
        rightLowerArmGeometry.setLocalTranslation(new Vector3f(
                0,
                leftUpperArm.yExtent / 2,
                0));
        
        Box leftLowerArm = new Box(body.xExtent / 6, body.yExtent, body.zExtent * 0.75f);
        Geometry leftLowerArmGeometry = new Geometry("Box", leftLowerArm);
        rightLowerArmGeometry.setLocalTranslation(new Vector3f(
                0,
                0,
                0));
        
        Box rightUpperLeg = new Box(body.xExtent / 6, body.yExtent, body.zExtent * 0.75f);
        Geometry rightUpperLegGeometry = new Geometry("Box", rightUpperLeg);
        rightUpperLegGeometry.setLocalTranslation(new Vector3f(
                0,
                 - rightUpperLeg.yExtent,
                0));
        
        Box rightLowerLeg = new Box(body.xExtent / 6, body.yExtent, body.zExtent * 0.75f);
        Geometry rightLowerLegGeometry = new Geometry("Box", rightLowerLeg);
        rightLowerLegGeometry.setLocalTranslation(new Vector3f(
                0,
                - rightLowerLeg.yExtent,
                0));
        
        Box leftUpperLeg = new Box(body.xExtent / 6, body.yExtent, body.zExtent * 0.75f);
        Geometry leftUpperLegGeometry = new Geometry("Box", leftUpperLeg);
        leftUpperLegGeometry.setLocalTranslation(new Vector3f(
                0,
                 - leftUpperLeg.yExtent,
                0));
        
        Box leftLowerLeg = new Box(body.xExtent / 6, body.yExtent, body.zExtent * 0.75f);
        Geometry leftLowerLegGeometry = new Geometry("Box", leftLowerLeg);
        leftLowerLegGeometry.setLocalTranslation(new Vector3f(
                0,
                - leftLowerLeg.yExtent,
                0));
        
        headGeometry.setMaterial(materials.get("head"));
        bodyGeometry.setMaterial(materials.get("body"));
        abdomenGeometry.setMaterial(materials.get("abdomen"));
        rightUpperArmGeometry.setMaterial(materials.get("upperArm"));
        leftUpperArmGeometry.setMaterial(materials.get("upperArm"));
        rightLowerArmGeometry.setMaterial(materials.get("lowerArm"));
        leftLowerArmGeometry.setMaterial(materials.get("lowerArm"));
        rightUpperLegGeometry.setMaterial(materials.get("upperLeg"));
        leftUpperLegGeometry.setMaterial(materials.get("upperLeg"));
        rightLowerLegGeometry.setMaterial(materials.get("lowerLeg"));
        leftLowerLegGeometry.setMaterial(materials.get("lowerLeg"));
        
        // HEAD
        
        Node headNode = new Node("head");
        headNode.setLocalTranslation(new Vector3f(
                0,
                head.yExtent,
                0
        ));
        headNode.attachChild(headGeometry);
        
        Node neckNode = new Node("neck");
        neckNode.setLocalTranslation(new Vector3f(
                0,
                body.yExtent ,
                0
        ));
        neckNode.attachChild(headNode);
        
        //ARMS
        
        //LEFT ARM
        
        Node leftLowerArmNode = new Node("leftLowerArm");
        leftLowerArmNode.setLocalTranslation(new Vector3f(
                0,
                - leftLowerArm.yExtent,
                0
        ));
        leftLowerArmNode.attachChild(leftLowerArmGeometry);
        
        Node leftElbowNode = new Node("leftElbow");
        leftElbowNode.setLocalTranslation(new Vector3f(
                0,
                - leftUpperArm.yExtent,
                0
        ));
        leftElbowNode.attachChild(leftLowerArmNode);
        
        Node leftUpperArmNode = new Node("leftUpperArm");
        leftUpperArmNode.setLocalTranslation(new Vector3f(
                0,
                - leftUpperArm.yExtent,
                0
        ));
        leftUpperArmNode.attachChild(leftUpperArmGeometry);
        leftUpperArmNode.attachChild(leftElbowNode);
        
        Node leftShoulderNode = new Node("leftShoulder");
        leftShoulderNode.setLocalTranslation(new Vector3f(
                 + body.xExtent + leftUpperArm.xExtent,
                body.yExtent,
                0
        ));
        leftShoulderNode.attachChild(leftUpperArmNode);
        
        //RIGHT ARM
        
        Node rightLowerArmNode = new Node("rightLowerArm");
        rightLowerArmNode.setLocalTranslation(new Vector3f(
                0,
                - rightLowerArm.yExtent,
                0
        ));
        rightLowerArmNode.attachChild(rightLowerArmGeometry);
        
        Node rightElbowNode = new Node("rightElbow");
        rightElbowNode.setLocalTranslation(new Vector3f(
                0,
                - rightUpperArm.yExtent,
                0
        ));
        rightElbowNode.attachChild(rightLowerArmNode);
               
        Node rightUpperArmNode = new Node("rightUpperArm");
        rightUpperArmNode.setLocalTranslation(new Vector3f(
                0,
                - rightUpperArm.yExtent,
                0
        ));
        rightUpperArmNode.attachChild(rightUpperArmGeometry);
        rightUpperArmNode.attachChild(rightElbowNode);
        
        Node rightShoulderNode = new Node("rightShoulder");
        rightShoulderNode.setLocalTranslation(new Vector3f(
                 - body.xExtent - rightUpperArm.xExtent,
                body.yExtent,
                0
        ));
        rightShoulderNode.attachChild(rightUpperArmNode);
        
        //LEGS
        
        //LEFT LEG
        Node leftLowerLegNode = new Node("leftLowerLeg");
        leftLowerLegNode.setLocalTranslation(new Vector3f(
                0,
                - leftLowerLeg.yExtent,
                0
        ));
        leftLowerLegNode.attachChild(leftLowerLegGeometry);
        
        Node leftKneeNode = new Node("leftKnee");
        leftKneeNode.setLocalTranslation(new Vector3f(
                0,
                - leftUpperLeg.yExtent,
                0
        ));
        leftKneeNode.attachChild(leftLowerLegNode);
        
        Node leftUpperLegNode = new Node("leftUpperLeg");
        leftUpperLegNode.setLocalTranslation(new Vector3f(
                abdomen.xExtent - leftUpperLeg.xExtent,
                - leftUpperLeg.yExtent,
                0
        ));
        leftUpperLegNode.attachChild(leftKneeNode);
        leftUpperLegNode.attachChild(leftUpperLegGeometry);
        
        //RIGHT LEG
        Node rightLowerLegNode = new Node("rightLowerLeg");
        rightLowerLegNode.setLocalTranslation(new Vector3f(
                0,
                - rightLowerLeg.yExtent,
                0
        ));
        rightLowerLegNode.attachChild(rightLowerLegGeometry);
        
        Node rightKneeNode = new Node("rightKnee");
        rightKneeNode.setLocalTranslation(new Vector3f(
                0,
                - rightUpperLeg.yExtent,
                0
        ));
        rightKneeNode.attachChild(rightLowerLegNode);
        
        Node rightUpperLegNode = new Node("rightUpperLeg");
        rightUpperLegNode.setLocalTranslation(new Vector3f(
                - abdomen.xExtent + rightUpperLeg.xExtent,
                - rightUpperLeg.yExtent,
                0
        ));
        rightUpperLegNode.attachChild(rightKneeNode);
        rightUpperLegNode.attachChild(rightUpperLegGeometry);
        
        //ABDOMEN
        Node abdomenNode = new Node("abdomen");
        abdomenNode.setLocalTranslation(new Vector3f(
                0,
                - body.yExtent,
                0
        ));
        abdomenNode.attachChild(abdomenGeometry);
        abdomenNode.attachChild(leftUpperLegNode);
        abdomenNode.attachChild(rightUpperLegNode);
        
        Node bodyNode = new Node("body");
        bodyNode.setLocalTranslation(new Vector3f(0.0f, 0.0f, 0.0f));
        bodyNode.attachChild(bodyGeometry);
        bodyNode.attachChild(neckNode);
        bodyNode.attachChild(leftShoulderNode);
        bodyNode.attachChild(rightShoulderNode);
        bodyNode.attachChild(abdomenNode);
        
        //abdomenNode.rotate(.0f, .0f, .0f);
        //neckNode.rotate(.0f, .0f, -.0f);
        
        //rightUpperLegNode.rotate(.0f, .0f, .0f);
        //leftUpperLegNode.rotate(.0f, .0f, .0f);
        
        //rightLowerLegNode.rotate(1.0f, .0f, .0f);
        //leftLowerLegNode.rotate(-1.0f, .0f, .0f);
        
        
        rootNode.attachChild(bodyNode);
        
    }

    @Override
    public void simpleUpdate(float tpf) {
        //TODO: add update code
        Float multiplier = 0.3f;
        if (this.liftLeft)
        {
            multiplier *= -1f;
        }
        rootNode.getChild("abdomen").rotate(.0f, multiplier * 0.0125f, .0f);
        rootNode.getChild("neck").rotate(.0f, .0f, multiplier * 0.03f);
        
        rootNode.getChild("leftUpperLeg").rotate(multiplier * 0.1f, 0, 0);
        rootNode.getChild("leftLowerLeg").rotate(-multiplier * 0.05f, 0, 0);
        rootNode.getChild("rightUpperLeg").rotate(-multiplier * 0.1f, 0, 0);
        rootNode.getChild("rightLowerLeg").rotate(multiplier * 0.05f, 0, 0);
        
        rootNode.getChild("rightShoulder").rotate(multiplier * 0.05f, 0, 0);
        rootNode.getChild("rightElbow").rotate(-multiplier * 0.025f, 0, 0);
        rootNode.getChild("leftShoulder").rotate(-multiplier * 0.05f, 0, 0);
        rootNode.getChild("leftElbow").rotate(multiplier * 0.025f, 0, 0);
        this.framesLeft -= 1;
        if (this.framesLeft == 0) {
            this.liftLeft = !this.liftLeft;
            this.framesLeft = 60;
        }
    }

    @Override
    public void simpleRender(RenderManager rm) {
        //TODO: add render code
    }
}
