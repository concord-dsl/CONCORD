import io.circe.Json
import io.circe.syntax._
import cats.syntax.either._
import io.circe._, io.circe.parser._ 
import java.io.File

def isSimpleAssignment(node: AstNode): Boolean = {
    /*
    * Conditions for an AstNode to be considered as simple assignment:
    * - The left subtree should be of size one and its node should be of type identifier (this is self evident) -> cond1.
    * - The right subtree leaf nodes should all be of type Literal -> cond1.
    * - All intermediate nodes should arithmetic or logical operations -> cond2.
    */
    val arithmetric_ops = Set("<operator>.modulo", "<operator>.subtraction", "<operator>.addition",
                                "<operator>.division", "<operator>.exponentiation", "<operator>.multiplication");
    val bitwise_ops = Set("<operator>.not", "<operator>.and", "<operator>.xor", "<operator>.or", 
                             "<operator>.shiftLeft",  "<operator>.shiftRight");
    val logical_ops = Set("<operator>.logicalNot", "<operator>.logicalOr", "<operator>.logicalAnd");
    val relational_ops = Set("<operator>.equals", "<operator>.notEquals", "<operator>.greaterThan", 
                                "<operator>.lessThan", "<operator>.greaterEqualsThan", "<operator>.lessEqualsThan");

    val allOps = arithmetric_ops ++ bitwise_ops ++ logical_ops ++ relational_ops;

    val astNodes = node.astMinusRoot.l;
    val cond1 = astNodes.count(_.isIdentifier) == 1;
    // If there exist a node in the right subtree with type not in allOps, then it's not a simple assignment.
    // e.g could be a method call (int a = foo(5)) or an array initializer (bool[] k = new bool[]{true, false})
    // Explanation of the traversal:
    //      - Look at none-leaf nodes first (count(children) == 0).
    //      - Check if their type is in allOps.
    val rightSubtreeNodes = astNodes.slice(1, astNodes.size);
    val nonLeafNodes = rightSubtreeNodes.filter(_.astChildren.size != 0);
    val cond2 = nonLeafNodes.count(n => (!allOps(n.propertiesMap.get("NAME").toString))) == 0;
    val leafNodes = rightSubtreeNodes.filter(_.astChildren.size == 0);
    val cond3 = astNodes.count(_.isLiteral) == leafNodes.size;

    return cond1 && cond2 && cond3;

}

@main def exec(output: String) = {
    val methods = cpg.method.filter(m => (m.filename != "<empty>" && !m.isExternal));
    val simpleAssignmentNodes = methods.map(_.astMinusRoot.filter(n => (n.propertiesMap.get("NAME")!=null && n.code != "<empty>"))
                                                          .filter(_.propertiesMap.get("NAME").toString.equalsIgnoreCase("<operator>.assignment"))
                                                          .filter(isSimpleAssignment)
                                                          .map(x => (x.file.l(0).name, (x.lineNumber.toList.l(0), x.code) )).l);
    val filePath = new File(output,"simple_assignment_stmnts.json").getPath;
    simpleAssignmentNodes.toList.filter(_.size != 0).flatten.groupBy(_._1).map(p => (p._1, p._2.map(_._2))).toMap.asJson.toString |> filePath;
}
